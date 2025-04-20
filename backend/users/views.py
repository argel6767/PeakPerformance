from .serializers import (
    CustomUserSerializer, RegisterUserSerializer, LoginUserSerializer,
    TwoFactorVerifySerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer, FriendRequestSerializer
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
from .serializers import FriendshipsSerializer

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
        serializer = LoginUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            
            UserEmailService.send_2fa_code(user)
            
            return Response({
                "message": "A verification code has been sent to your email",
                "email": user.email
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request):
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

class SendFriendRequestView(APIView):
    
    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Grab user doing request
            from_user = request.user
            # The recipient is fetched using the email from the serializer
            to_email = serializer.validated_data['email']
            to_user = CustomUser.objects.get(email=to_email)
            pending = from_user.send_friend_request(to_user)
            return Response({"success": f"Friend request sent: {pending}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptFriendRequestView(APIView):
    
    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            #Grab user doing request
            from_user = request.user
            # The recipient is fetched using the email from the serializer
            to_email = serializer.validated_data['email']
            to_user = CustomUser.objects.get(email=to_email)
            accepted = to_user.accept_friend_request(from_user=from_user)
            return Response({'success': f'Friend request accepted! {accepted}'}, status=status.HTTP_STATUS_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RejectFriendRequestView(APIView):
    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            #Grab user doing request
            from_user = request.user
            # The recipient is fetched using the email from the serializer
            to_email = serializer.validated_data['email']
            to_user = CustomUser.objects.get(email=to_email)
            accepted = to_user.reject_friend_request(from_user=from_user)
            return Response({'success': f'Friend request rejected! {accepted}'}, status=status.HTTP_STATUS_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Gets all a users status type, ie all pending, all accepted, deleted, blocked etc
'''
class GetAllStatusTypesRelationsView(APIView):
    
    def get(self, request):
        from_user = request.user
        status_type = request.query_params.get('status-type')
        if (status_type is None):
            return Response({'error': 'No status type given'}, status=status.HTTP_400_BAD_REQUEST)

        relations = [] # list of user's relations of a specifc type
        if (status_type == 'pending'):
            relations.append(from_user.get_pending_requests())
        elif (status_type == 'accepted'):
            relations.append(from_user.get_all_friends)
        
        serializer = FriendshipsSerializer(relations, many=True)
        return Response({'success': serializer.data}, status=status.HTTP_STATUS_200_OK)

class UnFriendUserViews(APIView):
    
    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            #Grab user doing request
            from_user = request.user
            # The recipient is fetched using the email from the serializer
            to_email = serializer.validated_data['email']
            friend_user = CustomUser.objects.get(email=to_email)
            from_user.unfriend_user(friend_user)
            return Response({'success': f'User: {to_email}, successfully un-added!'}, status=status.HTTP_STATUS_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
