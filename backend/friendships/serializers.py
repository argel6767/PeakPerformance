from users.models import CustomUser
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

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
