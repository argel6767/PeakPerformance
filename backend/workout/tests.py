from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from workout.models import Set, Workout, WorkoutExercise
from users.models import CustomUser, UserWeight
from movement.models import Movement, Muscle
from datetime import datetime, timedelta
from workout.analysis import *

# Create your tests here.
class AnalysisTestCase(TestCase):

    def setUp(self):
        self.userWeight = UserWeight(user=None, weight=400.20, created_at=datetime.now()) # No need to connect to an actual CustomUser Instance
        self.sets1 = [Set(weight=300.25, reps=10, workout_exercise_id=1, order=1),
            Set(weight=200.25, reps=10, workout_exercise_id=1, order=2),
            Set(weight=150.00, reps=10, workout_exercise_id=1, order=2)]
        self.sets2 = [Set(weight=250.00, reps=7, workout_exercise_id=1, order=4),
            Set(weight=200, reps=5, workout_exercise_id=1, order=5),
            Set(weight=100, reps=10, workout_exercise_id=1, order=6)]
        self.set = self.sets1[0]
        self.expected_orm = (lambda top_set: top_set.weight * (1 + (top_set.reps/30)))(self.set)

    def test_calculate_total_weight_volume(self):
        expected_volume = 6505
        self.assertEqual(expected_volume, calculate_total_weight_volume(self.sets1))

    def test_calculate_progress_overload_rate(self):
        total_volume_one = 6505
        total_volume_two = 3750
        expected_rate = (total_volume_one - total_volume_two)/ total_volume_two
        self.assertEqual(expected_rate, calculate_progress_overload_rate(initial_total_volume=total_volume_two, current_total_volume=total_volume_one))
    
    def test_calculate_epley_formula(self):
        self.assertEqual(self.expected_orm, calculate_epley_formula(top_set=self.set))

    def test_calculate_relative_strength(self):
        expected_relative_strength = self.expected_orm / self.userWeight.weight
        self.assertEqual(expected_relative_strength, calculate_relative_strength(self.expected_orm, self.userWeight))

class WorkoutAPITest(APITestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@example.com',
            username='user',
            password='password',
            is_staff=False
        )
        
        self.workout = Workout.objects.create(
            user = self.user,
            duration = '00:30:23',
            date = '2025-12-23'
        )
        
        self.initial_workout = Workout.objects.create(
            user = self.user,
            duration = '00:00:00',
            date = '2025-12-23'
        )
        
        self.muscle = Muscle.objects.create(
            name = 'Biceps',
            category = 'arms'
        )
        
        self.movement = Movement.objects.create(
        name='Supinated Curls',
        type='strength',
        movement_image_url='https://image.com'
    )

        # set the many-to-many relationship
        self.movement.muscles_worked.set([self.muscle])
        
        self.workout_exercise = WorkoutExercise.objects.create(
            workout = self.workout,
            movement = self.movement,
            order = 0
        )
        
        self.workout_dto_all_values = {
            'date': '2020-01-01',
            'duration': '01:23:34'
        }
        
        self.workout_dto_no_date = {
            'duration': '01:23:34'
        }
        
        self.workout_dto_no_duration = {
            'date': '2020-01-01'
        }
        
        self.workout_exercise_dto = {
            'workout' : self.workout,
            'movement' : self.movement,
            'order' : 1
        }
        
        self.set_dto = {
            'weight': 40,
            'reps': 9,
            'workout_exercise': self.workout_exercise,
            'order' : 1
        }
        
    def test_create_workout_entry(self):
        #Arrange
        self.client.force_login(user=self.user)
        
        #Acr
        response  = self.client.post('/api/workouts/', self.workout_dto_all_values, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 3)
        
        #Check DB
        workout = Workout.objects.get(user = self.user, duration='01:23:34')
        self.assertEqual(workout.user, self.user)
        self.assertEqual(workout.duration, timedelta('01:23:34'))
        self.assertEqual(workout.date, '2020-01-01')
        