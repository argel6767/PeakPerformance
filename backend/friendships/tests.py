from rest_framework.test import APITestCase
from users.models import CustomUser, Friendship
from rest_framework import status


# Create your tests here.
class FriendshipAPITest(APITestCase):
    def setUp(self):
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
        
        self.unknown_user_dto = {'email':'unknown@example.com'}
        
        self.request_dto1 = {
            'email':self.test_user.email
        }
        
        self.request_dto2 = {
            'email':self.test_user2.email
        }
        
    def _create_friendship_entry(self, status):
        # Helper to create a pending friendship
        return Friendship.objects.create(
            user=self.test_user2,
            friend=self.test_user,
            status=status
        )
    
    def test_send_friend_request(self):
        #Arrange
        self.client.force_authenticate(user=self.test_user)
        
        #Act
        response = self.client.post('/api/friends/send-request/', self.request_dto2, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Friendship.objects.count(), 1)
        
        #check DB
        new_friendship_entry = Friendship.objects.get(status = 'pending')
        self.assertEqual(new_friendship_entry.user, self.test_user)
        self.assertEqual(new_friendship_entry.friend, self.test_user2)
    
    def test_send_friend_request_to_self(self):
        #Arrange
        self.client.force_authenticate(user=self.test_user)
        
        #Act
        response = self.client.post('/api/friends/send-request/', self.request_dto1, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(Friendship.objects.count(), 0)
    
    def test_send_friend_request_to_non_existing_user(self):
        #Arrange
        self.client.force_authenticate(user=self.test_user)
        
        #Act
        response = self.client.post('/api/friends/send-request/', self.unknown_user_dto, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Friendship.objects.count(), 0)

    def test_accept_friend_request(self):
        #Arrange
        self.client.force_authenticate(user=self.test_user)
        
        #Act
        response = self.client.post('/api/friends/accept-request/', self.request_dto2, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Friendship.objects.count(), 1)
        
        #check DB
        new_friendship_entry = Friendship.objects.get(status = 'accepted')
        self.assertEqual(new_friendship_entry.user, self.test_user2) # user2 is the one who requested
        self.assertEqual(new_friendship_entry.friend, self.test_user)
        
    def test_accept_friend_request_to_self(self):
        #Arrange
        self.client.force_authenticate(user=self.test_user)
        
        #Act
        response = self.client.post('/api/friends/accept-request/', self.request_dto1, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(Friendship.objects.count(), 0)

    def test_accept_friend_request_to_non_existing_user(self):
        #Arrange
        self.client.force_authenticate(user=self.test_user)
        
        #Act
        response = self.client.post('/api/friends/accept-request/', self.unknown_user_dto, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Friendship.objects.count(), 0)
        
    def test_reject_friend_request(self):
        #Arrange
        self._create_friendship_entry(status='pending')
        self.client.force_authenticate(user=self.test_user)
        #Act
        response = self.client.post('/api/friends/reject-request/', self.request_dto2, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Friendship.objects.count(), 1)
        
        #check DB
        new_friendship_entry = Friendship.objects.get(status='rejected')
        self.assertEqual(new_friendship_entry.user, self.test_user2)  # Sender
        self.assertEqual(new_friendship_entry.friend, self.test_user)  # Receiver
        
    def test_reject_friend_request_to_self(self):
        #Arrange
        self.client.force_authenticate(user=self.test_user)
        
        #Act
        response = self.client.post('/api/friends/reject-request/', self.request_dto1, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(Friendship.objects.count(), 0)
        
    def test_reject_friend_request_to_non_existing_user(self):
        #Arrange
        self.client.force_authenticate(user=self.test_user)
        
        #Act
        response = self.client.post('/api/friends/reject-request/', self.unknown_user_dto, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Friendship.objects.count(), 0)

    def test_get_all_status_types_relations(self):
        #Arrange
        self._create_friendship_entry(status='accepted')
        self.client.force_authenticate(user=self.test_user2)
        
        #Act
        response = self.client.get('/api/friends/?status=accepted')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.data['success']
        self.assertEqual(body[0]['friend_email'], self.test_user.email)
        self.assertEqual(len(response.data['success']), 1)
        
    
    def test_unfriend_user(self):
        #Arrange
        self._create_friendship_entry(status='accepted')
        self.client.force_authenticate(self.test_user)
        
        #Act
        response = self.client.post('/api/friends/un-friend', self.request_dto2, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['success'], f'User: {self.test_user2.email}, successfully un-added!')

        #check db
        self.assertRaises(Friendship.DoesNotExist, lambda: Friendship.objects.get(status='accepted'))
        self.assertEqual(Friendship.objects.count(), 0)
        
    def test_unfriend_user_to_self(self):
        #Arrange
        self._create_friendship_entry(status='accepted')
        self.client.force_authenticate(self.test_user)
        
        #Act
        response = self.client.post('/api/friends/un-friend', self.request_dto1, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(Friendship.objects.count(), 1)

    def test_unfriend_user_to_non_existent_user(self):
        #Arrange
        self._create_friendship_entry(status='accepted')
        self.client.force_authenticate(self.test_user)

        #Act
        response = self.client.post('/api/friends/un-friend', self.unknown_user_dto, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Friendship.objects.count(), 1)