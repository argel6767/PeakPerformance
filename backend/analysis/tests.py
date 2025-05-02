from datetime import datetime, timedelta
from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from rest_framework import status
from rest_framework.test import APIClient

from analysis.analysis import *
from analysis.services import get_progressive_overload_rate, get_one_rep_max_for_movement
from analysis.errors import *
from users.models import UserWeight
from workout.models import Workout, WorkoutExercise, Set
from movement.models import Movement, Muscle

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

class ServicesTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.muscle = Muscle.objects.create(
            name='Chest',
            category='chest'
        )
        
        # Create a test movement
        self.movement = Movement.objects.create(
            name='Bench Press',
            type='strength'
        )
        self.movement.muscles_worked.set([self.muscle])
        
        self.no_workout_movement = Movement.objects.create(
            name='Chest Fly',
            type='strength'
        )
        self.movement.muscles_worked.set([self.muscle])
        
        # Create test workouts with different dates
        self.today = datetime.now().date()
        self.week_ago = self.today - timedelta(days=7)
        self.two_weeks_ago = self.today - timedelta(days=14)
        
        # Create recent workout
        self.recent_workout = Workout.objects.create(
            user=self.user,
            date=self.today
        )
        
        # Create baseline workout
        self.baseline_workout = Workout.objects.create(
            user=self.user,
            date=self.two_weeks_ago
        )
        
        # Create workout exercises
        self.recent_exercise = WorkoutExercise.objects.create(
            workout=self.recent_workout,
            movement=self.movement,
            order=1
        )
        
        self.baseline_exercise = WorkoutExercise.objects.create(
            workout=self.baseline_workout,
            movement=self.movement,
            order=1
        )
        
        # Create sets for recent workout
        Set.objects.create(
            weight=135,
            reps=10,
            workout_exercise=self.recent_exercise,
            order=1
        )
        Set.objects.create(
            weight=155,
            reps=8,
            workout_exercise=self.recent_exercise,
            order=2
        )
        
        # Create sets for baseline workout
        Set.objects.create(
            weight=115,
            reps=10,
            workout_exercise=self.baseline_exercise,
            order=1
        )
        Set.objects.create(
            weight=135,
            reps=8,
            workout_exercise=self.baseline_exercise,
            order=2
        )

    def test_get_progress_overload_rate(self):
        # Test with valid data
        result = get_progressive_overload_rate(self.movement.id, weeks_ago=2, user=self.user)
        
        # Calculate expected values
        recent_volume = (135 * 10) + (155 * 8)  # 1350 + 1240 = 2590
        baseline_volume = (115 * 10) + (135 * 8)  # 1150 + 1080 = 2230
        expected_rate = (recent_volume - baseline_volume) / baseline_volume
        
        self.assertEqual(result.data['movement']['id'], self.movement.id)
        self.assertEqual(result.data['baseline_week_volume'], baseline_volume)
        self.assertEqual(result.data['most_recent_week_volume'], recent_volume)
        self.assertEqual(result.data['progressive_overload_change'], expected_rate)
        self.assertEqual(result.data['week_difference'], 2)
        
        # Test with invalid id
        with self.assertRaises(NoMovementEntryFoundError):
            get_progressive_overload_rate(9999, weeks_ago=10, user=self.user)
        
        # Test with invalid date range (no workouts in that period)
        with self.assertRaises(InvalidDateRangeError):
            get_progressive_overload_rate(self.movement.id, weeks_ago=10, user=self.user)

    def test_get_one_rep_max_for_movement(self):
        # Test with valid data
        result = get_one_rep_max_for_movement(self.movement.id, self.user)
        
        # The highest performing set is 155 lbs for 8 reps
        # Using Epley formula: weight * (1 + (epley constant * reps))
        expected_orm = 135 * (1 + (EPLEY_CONSTANT * 10))
        
        self.assertEqual(result.data['movement']['id'], self.movement.id)
        self.assertEqual(result.data['estimated_orm'], expected_orm)
        
        # Test with non-existent movement
        with self.assertRaises(NoMovementEntryFoundError):
            get_one_rep_max_for_movement(999, self.user)  # Non-existent movement ID
            
        # Test with movement that does not exist
        movement_no_sets = Movement.objects.create(
            name='No Sets Movement',
            type='cardio'
        )
        movement_no_sets.muscles_worked.set([self.muscle])
        exercise_no_sets = WorkoutExercise.objects.create(
            workout=self.recent_workout,
            movement=movement_no_sets,
            order=2
        )
        
        with self.assertRaises(NoExerciseEntryFoundError):
            get_one_rep_max_for_movement(self.no_workout_movement.id, self.user)
            
        with self.assertRaises(NoSetEntriesFoundError):
            get_one_rep_max_for_movement(movement_no_sets.id, self.user)

class ViewsTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.muscle = Muscle.objects.create(
            name='Chest',
            category='chest'
        )
        
        # Create a test movement
        self.movement = Movement.objects.create(
            name='Bench Press',
            type='strength'
        )
        self.movement.muscles_worked.set([self.muscle])
        
        # Create test workouts with different dates
        self.today = datetime.now().date()
        self.week_ago = self.today - timedelta(days=7)
        self.two_weeks_ago = self.today - timedelta(days=14)
        
        # Create recent workout
        self.recent_workout = Workout.objects.create(
            user=self.user,
            date=self.today
        )
        
        # Create baseline workout
        self.baseline_workout = Workout.objects.create(
            user=self.user,
            date=self.two_weeks_ago
        )
        
        # Create workout exercises
        self.recent_exercise = WorkoutExercise.objects.create(
            workout=self.recent_workout,
            movement=self.movement,
            order=1
        )
        
        self.baseline_exercise = WorkoutExercise.objects.create(
            workout=self.baseline_workout,
            movement=self.movement,
            order=1
        )
        
        # Create sets for recent workout
        Set.objects.create(
            weight=135,
            reps=10,
            workout_exercise=self.recent_exercise,
            order=1
        )
        Set.objects.create(
            weight=155,
            reps=8,
            workout_exercise=self.recent_exercise,
            order=2
        )
        
        # Create sets for baseline workout
        Set.objects.create(
            weight=115,
            reps=10,
            workout_exercise=self.baseline_exercise,
            order=1
        )
        Set.objects.create(
            weight=135,
            reps=8,
            workout_exercise=self.baseline_exercise,
            order=2
        )

        # Force authentication for the test client
        self.client.force_authenticate(user=self.user)

    def test_get_progressive_overload_success(self):
        url = reverse('get-progressive-overload')
        response = self.client.get(f'{url}?movement_id={self.movement.id}&weeks_ago=2')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('movement', response.data)
        self.assertIn('baseline_week_volume', response.data)
        self.assertIn('most_recent_week_volume', response.data)
        self.assertIn('progressive_overload_change', response.data)
        self.assertIn('week_difference', response.data)

    def test_get_progressive_overload_invalid_movement(self):
        url = reverse('get-progressive-overload')
        response = self.client.get(f'{url}?movement_id=999&weeks_ago=2')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_get_progressive_overload_invalid_weeks(self):
        url = reverse('get-progressive-overload')
        response = self.client.get(f'{url}?movement_id={self.movement.id}&weeks_ago=invalid')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_get_progressive_overload_missing_params(self):
        url = reverse('get-progressive-overload')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_get_orm_success(self):
        url = reverse('get-one-rep-max', args=[self.movement.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('movement', response.data)
        self.assertIn('estimated_orm', response.data)

    def test_get_orm_invalid_movement(self):
        url = reverse('get-one-rep-max', args=[999])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_get_orm_unauthorized(self):
        # Create a new client without authentication
        client = APIClient()
        url = reverse('get-one-rep-max', args=[self.movement.id])
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_progressive_overload_unauthorized(self):
        # Create a new client without authentication
        client = APIClient()
        url = reverse('get-progressive-overload')
        response = client.get(f'{url}?movement_id={self.movement.id}&weeks_ago=2')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)