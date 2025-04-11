from rest_framework.test import APITestCase
from rest_framework import status

from users.models import CustomUser

from .models import Muscle, Movement


# Create your tests here.
class MovementAPITest(APITestCase):

    def setUp(self):
        # Create admin user
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='password123',
            is_staff=True
        )
        self.user = CustomUser.objects.create_user(
            email='user@example.com',
            username='user',
            password='password',
            is_staff=False
        )
        #use for later
        muscle, _ = Muscle.objects.get_or_create(
            name = 'Biceps',
            category = 'arms'
        )
        self.biceps = muscle
        
        muscle2, _ = Muscle.objects.get_or_create(
            name = 'Hamstring',
            category = 'legs'
        )
        self.hamstrings = muscle2
        
        #create Dtos
        self.muscleDto = {
            'name':'Triceps',
            'category':'arms'
        }
        
        self.muscleDto2 = {
            'name':'Upper-Chest',
            'category':'Chest'
        }
        
        self.movementDto = {
            'name':'Supinated Curls',
            'muscles_worked':[self.biceps.pk],
            'type':'strength',
            'movement_image_url':'https://image.com/supinated-curls'
        }
        
        self.movementDto2 = {
            'name':'Romanian Deadlift',
            'muscles_worked':[self.hamstrings.pk],
            'type':'strength',
            'movement_image_url':'https://image.com/supinated-curls'
        }

    def test_create_muscle_entry(self):
        #Arrange
        self.client.force_authenticate(user=self.admin)
        
        #Act
        response = self.client.post('/api/muscles/', self.muscleDto, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Muscle.objects.count(), 3)
        
        #check DB
        new_muscle_entry = Muscle.objects.get(name = 'Triceps')
        self.assertEqual(new_muscle_entry.name, 'Triceps')
        self.assertEqual(new_muscle_entry.category, 'arms')

    def test_create_muscle_entry_by_non_admin(self):
        #Arrange
        self.client.force_login(self.user)
        
        #Act
        response = self.client.post('/api/muscles/', self.muscleDto, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Muscle.objects.count(), 2)
        self.assertRaises(Muscle.DoesNotExist, lambda: Muscle.objects.get(name = 'Upper-Chest'))

    def test_create_movement_entry(self):
        #Arrange
        self.client.force_authenticate(user=self.admin)
        
        #Act
        response = self.client.post('/api/movements/', self.movementDto, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movement.objects.count(), 1)
        
        #check DB
        new_movement_entry = Movement.objects.get(name='Supinated Curls')
        self.assertEqual(new_movement_entry.name, 'Supinated Curls')
        self.assertEqual(new_movement_entry.type, 'strength')
        muscle_ids = list(new_movement_entry.muscles_worked.values_list('id', flat=True)) # muscle table entries
        self.assertEqual(muscle_ids, [self.biceps.pk])
        self.assertEqual(new_movement_entry.movement_image_url, 'https://image.com/supinated-curls')

    def test_create_movement_entry_by_non_admin(self):
        #Arrange
        self.client.force_authenticate(user=self.user)
        
        #Act
        response = self.client.post('/api/movements/', self.movementDto2, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Movement.objects.count(), 0)
        self.assertRaises(Movement.DoesNotExist, lambda: Movement.objects.get(name = 'Romanian Deadlift'))

    def test_get_muscle_list(self):
        # Arrange
        self.client.force_authenticate(user=self.user)
        
        # Act
        response = self.client.get('/api/muscles/', format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should only return the two muscles created in setUp

    def test_get_muscle_detail(self):
        # Arrange
        self.client.force_authenticate(user=self.user)
        
        # Act
        response = self.client.get(f'/api/muscles/{self.biceps.pk}/', format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Biceps')
        self.assertEqual(response.data['category'], 'arms')

    def test_update_muscle_by_admin(self):
        # Arrange
        self.client.force_authenticate(user=self.admin)
        updated_data = {
            'name': 'Biceps Brachii',
            'category': 'arms'
        }
        
        # Act
        response = self.client.put(f'/api/muscles/{self.biceps.pk}/', updated_data, format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check DB
        updated_muscle = Muscle.objects.get(pk=self.biceps.pk)
        self.assertEqual(updated_muscle.name, 'Biceps Brachii')
        self.assertEqual(updated_muscle.category, 'arms')

    def test_update_muscle_by_non_admin(self):
        # Arrange
        self.client.force_authenticate(user=self.user)
        updated_data = {
            'name': 'Biceps Brachii',
            'category': 'upper arms'
        }
        
        # Act
        response = self.client.put(f'/api/muscles/{self.biceps.pk}/', updated_data, format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Check DB - should be unchanged
        unchanged_muscle = Muscle.objects.get(pk=self.biceps.pk)
        self.assertEqual(unchanged_muscle.name, 'Biceps')
        self.assertEqual(unchanged_muscle.category, 'arms')

    def test_delete_muscle_by_admin(self):
        # Arrange
        self.client.force_authenticate(user=self.admin)
        
        # Act
        response = self.client.delete(f'/api/muscles/{self.biceps.pk}/', format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Muscle.objects.count(), 1)  # Only hamstrings should remain
        self.assertRaises(Muscle.DoesNotExist, lambda: Muscle.objects.get(pk=self.biceps.pk))

    def test_delete_muscle_by_non_admin(self):
        # Arrange
        self.client.force_authenticate(user=self.user)
        
        # Act
        response = self.client.delete(f'/api/muscles/{self.biceps.pk}/', format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Muscle.objects.count(), 2)  # Both muscles should still exist

    # Now for Movement tests
    def test_get_movement_list(self):
        # Arrange - First create a movement to list
        self.client.force_authenticate(user=self.admin)
        self.client.post('/api/movements/', self.movementDto, format='json')
        
        # Force authenticate with regular user
        self.client.force_authenticate(user=self.user)
        
        # Act
        response = self.client.get('/api/movements/', format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_movement_detail(self):
        # Arrange - First create a movement
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/movements/', self.movementDto, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Get the movement from the database instead of response
        created_movement = Movement.objects.get(name=self.movementDto['name'])
        movement_id = created_movement.pk
        
        # Force authenticate with regular user
        self.client.force_authenticate(user=self.user)
        
        # Act
        response = self.client.get(f'/api/movements/{movement_id}/', format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Supinated Curls')
        self.assertEqual(response.data['type'], 'strength')
        self.assertEqual(response.data['movement_image_url'], 'https://image.com/supinated-curls')
        self.assertEqual(response.data['muscles_worked'], [self.biceps.pk])

    def test_update_movement_by_admin(self):
        # Arrange - First create a movement
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/movements/', self.movementDto, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Get the movement from the database
        created_movement = Movement.objects.get(name=self.movementDto['name'])
        movement_id = created_movement.pk
        
        updated_data = {
            'name': 'Hammer Curls',
            'muscles_worked': [self.biceps.pk],
            'type': 'strength',
            'movement_image_url': 'https://image.com/hammer-curls'
        }
        
        # Act
        response = self.client.put(f'/api/movements/{movement_id}/', updated_data, format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check DB
        updated_movement = Movement.objects.get(pk=movement_id)
        self.assertEqual(updated_movement.name, 'Hammer Curls')
        self.assertEqual(updated_movement.movement_image_url, 'https://image.com/hammer-curls')

    def test_update_movement_by_non_admin(self):
        # Arrange - First create a movement
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/movements/', self.movementDto, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Get the movement from the database
        created_movement = Movement.objects.get(name=self.movementDto['name'])
        movement_id = created_movement.pk
        
        # Switch to non-admin user
        self.client.force_authenticate(user=self.user)
        
        updated_data = {
            'name': 'Hammer Curls',
            'muscles_worked': [self.biceps.pk],
            'type': 'strength',
            'movement_image_url': 'https://image.com/hammer-curls'
        }
        
        # Act
        response = self.client.put(f'/api/movements/{movement_id}/', updated_data, format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Check DB - should be unchanged
        unchanged_movement = Movement.objects.get(pk=movement_id)
        self.assertEqual(unchanged_movement.name, 'Supinated Curls')

    def test_delete_movement_by_admin(self):
        # Arrange - First create a movement
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/movements/', self.movementDto, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Get the movement from the database
        created_movement = Movement.objects.get(name=self.movementDto['name'])
        movement_id = created_movement.pk
        
        # Act
        response = self.client.delete(f'/api/movements/{movement_id}/', format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movement.objects.count(), 0)
        self.assertRaises(Movement.DoesNotExist, lambda: Movement.objects.get(pk=movement_id))

    def test_delete_movement_by_non_admin(self):
        # Arrange - First create a movement
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/movements/', self.movementDto, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Get the movement from the database
        created_movement = Movement.objects.get(name=self.movementDto['name'])
        movement_id = created_movement.pk
    
        
        # Switch to non-admin user
        self.client.force_authenticate(user=self.user)
        
        # Act
        response = self.client.delete(f'/api/movements/{movement_id}/', format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Movement.objects.count(), 1)  # Movement should still exist