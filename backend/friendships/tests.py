from rest_framework.test import APITestCase
from users.models import CustomUser, Friendship
from rest_framework import status


# Create your tests here.
class FriendshipAPITest(APITestCase):
    def setup(self):
# Create test users
        self.test_user = CustomUser.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123'
        )
        
        self.test_user2 = CustomUser.objects.create_user(
            email='email@example.com',
            username='user123',
            password='password'
        )
        
        self.request_dto1 = {
            'email':self.test_user.email
        }
        
        self.request_dtow = {
            'email':self.test_user2.email
        }
    
    def test_send_friend_request(self):
        #Arrange
        self.client.force_authenticate(user=self.user)
        
        #Act
        response = self.client.post('api/friendships/send-request', self.request_dto2, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Friendship.objects.count(), 1)
        
        #check DB
        new_friendship_entry = Friendship.objects.get(status = 'pending')
        self.assertEquals(new_friendship_entry.user, self.test_user.pk)
        self.assertEquals(new_friendship_entry.friend, self.test_user2.pk)
