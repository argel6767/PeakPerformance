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
        #use for later
        muscle, _ = Muscle.objects.get_or_create(
            name = 'Biceps',
            category = 'arms'
        )
        self.biceps = muscle
        
        #create Dtos
        self.muscleDto = {
            'name':'Triceps',
            'category':'arms'
        }
        
        self.movementDto = {
            'name':'Supinated Curls',
            'muscles_worked':[self.biceps.pk],
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
        self.assertEqual(Muscle.objects.count(), 2)
        
        #check DB
        new_muscle_entry = Muscle.objects.get(name = 'Triceps')
        self.assertEqual(new_muscle_entry.name, 'Triceps')
        self.assertEqual(new_muscle_entry.category, 'arms')
    
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
        