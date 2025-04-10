from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, TwoFactorCode, PasswordResetToken
from datetime import timedelta

class UserAPITest(APITestCase):
    
    def setUp(self):
        # Create a test user
        self.test_user = CustomUser.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123'
        )
        
        # Setup valid data for testing
        self.valid_register_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'password123'
        }
        
        self.valid_login_data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }
    
    def test_create_user(self):
        """Test user registration"""
        response = self.client.post('/api/users/register/', self.valid_register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)  # Our test user + new user
        
        # Verify the new user exists with the correct details
        new_user = CustomUser.objects.get(email='newuser@example.com')
        self.assertEqual(new_user.username, 'newuser')
        self.assertTrue(new_user.check_password('password123'))

    def test_login_flow(self):
        """Test the two-factor authentication login flow"""
        # Step 1: Login request should return a message about 2FA code sent
        response = self.client.post('/api/users/login/', self.valid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('verification code', response.data['message'].lower())
        self.assertEqual(response.data['email'], 'testuser@example.com')
        
        # Check 2FA code was created
        self.assertTrue(TwoFactorCode.objects.filter(user=self.test_user).exists())
        
        # Step 2: Verify 2FA code
        code_obj = TwoFactorCode.objects.get(user=self.test_user)
        
        verify_data = {
            'email': 'testuser@example.com',
            'code': code_obj.code
        }
        
        response = self.client.post('/api/users/verify-2fa/', verify_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify response contains user data and cookies were set
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], self.test_user.username)
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)
        
        # Verify cookies have correct properties
        self.assertTrue(response.cookies['access_token']['httponly'])
        self.assertTrue(response.cookies['access_token']['secure'])
        self.assertEqual(response.cookies['access_token']['samesite'], 'None')
        self.assertTrue(response.cookies['refresh_token']['httponly'])
        self.assertTrue(response.cookies['refresh_token']['secure'])
        self.assertEqual(response.cookies['refresh_token']['samesite'], 'None')
        
        # Verify 2FA code was deleted after use
        self.assertFalse(TwoFactorCode.objects.filter(user=self.test_user).exists())
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        invalid_data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post('/api/users/login/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_invalid_2fa_code(self):
        """Test using an invalid 2FA code"""
        # First login to generate a 2FA code
        self.client.post('/api/users/login/', self.valid_login_data, format='json')
        
        # Try with wrong code
        invalid_verify_data = {
            'email': 'testuser@example.com',
            'code': '000000'  # Wrong code
        }
        
        response = self.client.post('/api/users/verify-2fa/', invalid_verify_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_expired_2fa_code(self):
        """Test using an expired 2FA code"""
        # First login to generate a 2FA code
        self.client.post('/api/users/login/', self.valid_login_data, format='json')
        
        # Get the code and manually expire it
        code_obj = TwoFactorCode.objects.get(user=self.test_user)
        code_obj.expires_at = timezone.now() - timedelta(minutes=1)
        code_obj.save()
        
        # Try to verify with expired code
        verify_data = {
            'email': 'testuser@example.com',
            'code': code_obj.code
        }
        
        response = self.client.post('/api/users/verify-2fa/', verify_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_logout(self):
        """Test user logout functionality"""
        # First login and get authenticated
        self.client.post('/api/users/login/', self.valid_login_data, format='json')
        code_obj = TwoFactorCode.objects.get(user=self.test_user)
        
        verify_data = {
            'email': 'testuser@example.com',
            'code': code_obj.code
        }
        
        self.client.post('/api/users/verify-2fa/', verify_data, format='json')
        
        # Then logout
        response = self.client.post('/api/users/logout/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify cookies were deleted
        self.assertFalse('access_token' in response.cookies or response.cookies['access_token'].value)
        self.assertFalse('refresh_token' in response.cookies or response.cookies['refresh_token'].value)
    
    def test_user_info(self):
        """Test retrieving user information"""
        # First authenticate the user
        self.client.force_authenticate(user=self.test_user)
        
        # Get user info
        response = self.client.get('/api/users/user-info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.test_user.email)
        self.assertEqual(response.data['username'], self.test_user.username)
    
    def test_token_refresh(self):
        """Test JWT token refresh functionality"""
        # First login and authenticate to get tokens
        self.client.post('/api/users/login/', self.valid_login_data, format='json')
        code_obj = TwoFactorCode.objects.get(user=self.test_user)
        
        verify_data = {
            'email': 'testuser@example.com',
            'code': code_obj.code
        }
        
        auth_response = self.client.post('/api/users/verify-2fa/', verify_data, format='json')
        
        # Force client to use the cookies from the auth response
        self.client.cookies = auth_response.cookies
        
        # Request a token refresh
        response = self.client.post('/api/users/refresh/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.cookies)
    
    def test_password_reset_request(self):
        """Test requesting a password reset"""
        # Request password reset
        response = self.client.post('/api/users/password-reset/', {'email': 'testuser@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify token was created
        self.assertTrue(PasswordResetToken.objects.filter(user=self.test_user).exists())
    
    def test_password_reset_invalid_email(self):
        """Test password reset with non-existent email"""
        # Request password reset with non-existent email
        response = self.client.post('/api/users/password-reset/', {'email': 'nonexistent@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_password_reset_confirm(self):
        """Test confirming a password reset"""
        # First request a password reset
        self.client.post('/api/users/password-reset/', {'email': 'testuser@example.com'}, format='json')
        
        # Get the token
        token_obj = PasswordResetToken.objects.get(user=self.test_user)
        
        # Confirm password reset
        reset_data = {
            'token': token_obj.token,
            'password': 'newpassword123'
        }
        
        response = self.client.post('/api/users/password-reset/confirm/', reset_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify password was changed
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.check_password('newpassword123'))
        
        # Verify token was deleted
        self.assertFalse(PasswordResetToken.objects.filter(user=self.test_user).exists())
    
    def test_password_reset_invalid_token(self):
        """Test password reset with invalid token"""
        # Try with invalid token
        reset_data = {
            'token': 'invalid-token',
            'password': 'newpassword123'
        }
        
        response = self.client.post('/api/users/password-reset/confirm/', reset_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_reset_expired_token(self):
        """Test password reset with expired token"""
        # First request a password reset
        self.client.post('/api/users/password-reset/', {'email': 'testuser@example.com'}, format='json')
        
        # Get the token and manually expire it
        token_obj = PasswordResetToken.objects.get(user=self.test_user)
        token_obj.expires_at = timezone.now() - timedelta(minutes=1)
        token_obj.save()
        
        # Try to confirm with expired token
        reset_data = {
            'token': token_obj.token,
            'password': 'newpassword123'
        }
        
        response = self.client.post('/api/users/password-reset/confirm/', reset_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)