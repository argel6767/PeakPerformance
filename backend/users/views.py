from datetime import timedelta
from .serializers import (
    CustomUserSerializer, RegisterUserSerializer, LoginUserSerializer,
    TwoFactorVerifySerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from django.shortcuts import get_object_or_404
from .models import CustomUser, PasswordResetToken
from .services import UserEmailService
from django.core.exceptions import BadRequest


# Create your views here.
class UserInfoView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user

class UserRegistrationView(CreateAPIView):
    serializer_class = RegisterUserSerializer

class LoginView(APIView):
    def post(self, request):
        source = request.headers.get("Source-Header")
        if not source:
            raise BadRequest("Source-Header required")

        serializer = LoginUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

        user = serializer.validated_data

        if source == "mobile":
            refresh = RefreshToken.for_user(user)
            refresh.set_exp(lifetime=timedelta(days=7)) #make long for mobile app users
            access_token = str(refresh.access_token)
            response = Response({
                "user": CustomUserSerializer(user).data,
                "access_token": access_token,
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)
            return response

        elif source == "web":
            UserEmailService.send_2fa_code(user)
            return Response({
                "message": "A verification code has been sent to your email",
                "email": user.email
            }, status=status.HTTP_200_OK)

        return Response({"error_message": "Invalid header given"}, status=status.HTTP_400_BAD_REQUEST)

class TwoFactorVerifyView(APIView):
    def post(self, request):
        serializer = TwoFactorVerifySerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            response = Response({
                "user": CustomUserSerializer(user).data
            }, status=status.HTTP_200_OK)
            
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None'
            )
            
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="None"
            )
            
            return response
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    def post(self, request):
        source = request.headers.get("Source-Header")
        if not source:
            raise BadRequest("Source-Header required")
        
        if source == 'mobile':
            refresh_token = request.headers.get("Refresh-Token")
            if refresh_token:
                try:
                    refresh = RefreshToken(refresh_token)
                    refresh.blacklist()
                except Exception as e:
                    return Response({'error':'Error invalidating the token.' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
                response = Response({'message': 'successfully logged out'})
                return response
            
        elif source == 'web':
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                try:
                    refresh = RefreshToken(refresh_token)
                    refresh.blacklist()
                except Exception as e:
                    return Response({'error':'Error invalidating the token.' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
            response = Response({'message': 'successfully logged out'})
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
        
        return Response({'error': "Invalid header"}, status=status.HTTP_400_BAD_REQUEST)


class UserTokenRefreshView(TokenRefreshView):
    def post(self, request):
        
        source = request.headers.get("Source-Header")
        if not source:
            raise BadRequest("Source-Header required")
        
        if source == "mobile":
            refresh_token = request.headers.get("Refresh-Token")
            
            if not refresh_token:
                return Response({'error':'Refresh token not provided'}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                refresh = RefreshToken(refresh_token)
                access_token = str(refresh.access_token)
                
                response = Response({'message':'Access token refresh successfully','access_token': access_token}, status=status.HTTP_200_OK)
                return response
            except InvalidToken:
                return Response({'error':'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
            
        elif source == "web":
            refresh_token = request.COOKIES.get('refresh_token')

            if not refresh_token:
                return Response({'error':'Refresh token not provided'}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                refresh = RefreshToken(refresh_token)
                access_token = str(refresh.access_token)

                response = Response({'message':'Access token refresh successfully'}, status=status.HTTP_200_OK)
                response.set_cookie(key='access_token',
                                    value = access_token,
                                    httponly=True,
                                    secure=True,
                                    samesite='None')
                return response
            except InvalidToken:
                return Response({'error':'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': "Invalid header"}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_object_or_404(CustomUser, email=email)
            
            UserEmailService.send_password_reset(user)
            
            return Response({
                "message": "Password reset instructions have been sent to your email"
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['password']
            
            token_obj = get_object_or_404(PasswordResetToken, token=token)
            
            if not token_obj.is_valid():
                token_obj.delete()
                return Response({
                    "error": "Reset token has expired"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = token_obj.user
            user.set_password(new_password)
            user.save()
            
            token_obj.delete()
            
            return Response({
                "message": "Password has been reset successfully"
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
