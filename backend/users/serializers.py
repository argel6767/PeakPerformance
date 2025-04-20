from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .models import CustomUser, TwoFactorCode, PasswordResetToken, Friendship
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username')

class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class LoginUserSerializer(Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect credentials')

class TwoFactorVerifySerializer(Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            
            try:
                code_obj = TwoFactorCode.objects.get(user=user, code=data['code'])
                
                if not code_obj.is_valid():
                    raise serializers.ValidationError('Code has expired')
                
                code_obj.delete()
                return user
            except TwoFactorCode.DoesNotExist:
                raise serializers.ValidationError('Invalid verification code')
                
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('User not found')

class PasswordResetRequestSerializer(Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            CustomUser.objects.get(email=value)
            return value
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('No user found with this email address')

class PasswordResetConfirmSerializer(Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate_token(self, value):
        try:
            token_obj = PasswordResetToken.objects.get(token=value)
            
            if not token_obj.is_valid():
                token_obj.delete()
                raise serializers.ValidationError('Reset token has expired')
                
            return value
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError('Invalid reset token')
    
    def validate_password(self, value):
        try:
            validate_password(value)
            return value
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        

class FriendRequestSerializer(Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        # Only validates that the email exists in the system, this is the email of the user the friend request is to, not sender
        try:
            CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        return value

# Shows the basic information about relationships between the user and others
class FriendshipsSerializer(ModelSerializer):
    friend_email = serializers.CharField(source='friend.email', read_only=True)
    friend_username = serializers.CharField(source='friend.username', read_only=True)
    
    class Meta:
        model = Friendship
        fields = ['id', 'friend_email', 'friend_username', 'status', 'created_at']
