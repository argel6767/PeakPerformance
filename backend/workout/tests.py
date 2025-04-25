from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from workout.models import Set, Workout, WorkoutExercise
from users.models import CustomUser, UserWeight
from movement.models import Movement, Muscle
from datetime import date, datetime, timedelta
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
        
        self.set = Set.objects.create(
            weight=100,
            reps = 10,
            workout_exercise = self.workout_exercise,
            order=0
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
        
        self.workout_exercise_dto = [{
            'workout' : self.workout.pk,
            'movement' : self.movement.pk,
            'order' : 1
        }]
        
        self.set_dto = [{
            'weight': 40,
            'reps': 9,
            'workout_exercise': self.workout_exercise.pk,
            'order' : 1
        }]
        
    def test_create_workout_entry(self):
        #Arrange
        self.client.force_login(user=self.user)
        
        #Act
        response  = self.client.post('/api/workouts/', self.workout_dto_all_values, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 3)
        
        #Check DB
        workout = Workout.objects.get(user = self.user, duration='01:23:34')
        self.assertEqual(workout.user, self.user)
        expected_duration = timedelta(hours=1, minutes=23, seconds=34)
        self.assertEqual(workout.duration, expected_duration)
        expected_date = date(2020, 1, 1)
        self.assertEqual(workout.date, expected_date)

    def test_create_workout_entry_by_non_authenticated_user(self):
        #Act
        response  = self.client.post('/api/workouts/', self.workout_dto_all_values, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Workout.objects.count(), 2)

    def test_create_workout_entry_with_no_duration_given(self):
        #Arrange
        self.client.force_login(self.user)
        
        #Act
        response = self.client.post('/api/workouts/', self.workout_dto_no_duration, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 3)

        #Check DB
        workout = Workout.objects.get(user = self.user, date='2020-01-01')
        expected_date = date(2020, 1, 1)
        self.assertEqual(workout.date, expected_date)
        self.assertEqual(workout.duration, timedelta(seconds=0))

    def test_create_workout_entry_with_no_date_given(self):
        #Arrange
        self.client.force_login(self.user)
            
        #Act
        response = self.client.post('/api/workouts/', self.workout_dto_no_date, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 3)

        #Check DB
        workout = Workout.objects.get(user = self.user, duration='01:23:34')
        expected_duration = timedelta(hours=1, minutes=23, seconds=34)
        self.assertEqual(workout.duration, expected_duration)
        expected_date = date.today()
        self.assertEqual(workout.date, expected_date)

    def test_update_initial_workout_entry(self):
        #Arrange
        initial_workout = Workout.objects.get(duration='00:00:00')
        initial_pk = initial_workout.pk
        self.client.force_login(self.user)
        
        # Create a dictionary with the updated data
        updated_data = {
            'duration': '01:10:34',
            'date': '2025-12-23'
        }
        
        #Act
        response = self.client.put(f'/api/workouts/{initial_pk}/', updated_data, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Workout.objects.count(), 2) #should be no change as its an update
        
        # Check DB
        updated_workout = Workout.objects.get(pk=initial_pk)
        self.assertEqual(updated_workout.duration, timedelta(hours=1, minutes=10, seconds=34))
        self.assertNotEqual(initial_workout.duration, updated_workout.duration)

    def test_delete_workout_entry(self):
        #Arrange
        self.client.force_login(self.user)
        workout_pk = self.workout.pk

        #Act
        response = self.client.delete(f'/api/workouts/{workout_pk}/')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Workout.objects.count(), 1)
        
        #Check DB
        self.assertRaises(Workout.DoesNotExist, lambda: Workout.objects.get(pk=workout_pk))
        
    def test_create_workout_exercise_entry_for_a_workout(self):
        #Arrange
        self.client.force_login(self.user)

        #Act
        response = self.client.post('/api/exercises/', self.workout_exercise_dto, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkoutExercise.objects.count(), 2)
        
        #Check DB
        workout_exercise = WorkoutExercise.objects.get(order=1)
        parent_workout = workout_exercise.workout
        self.assertEqual(parent_workout, self.workout)
        self.assertEqual(workout_exercise.movement, self.movement)
    
    def test_create_multiple_workout_exercise_entry_for_a_workout(self):
        #Arrange
        exercises_data = [
        {
            'workout': self.workout.pk,
            'movement': self.movement.pk,
            'order': 1
        },
        {
            'workout': self.workout.pk,
            'movement': self.movement.pk,
            'order': 2
        }
        ]
        self.client.force_login(self.user)
        
        #Act
        response = self.client.post('/api/exercises/', exercises_data, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkoutExercise.objects.count(), 3)

        #Check DB
        workout_exercise1 = WorkoutExercise.objects.get(order=1)
        workout_exercise2 = WorkoutExercise.objects.get(order=2)
        self.assertEqual(workout_exercise1.workout, self.workout)
        self.assertEqual(workout_exercise2.workout, self.workout)
        self.assertEqual(workout_exercise1.movement.pk, exercises_data[0]['movement'])
        self.assertEqual(workout_exercise2.movement.pk, exercises_data[1]['movement'])

    def test_create_workout_exercise_by_unauthenticated_user(self):
        #Act
        response = self.client.post('/api/exercises/', self.workout_exercise_dto, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(WorkoutExercise.objects.count(), 1)
        
    def test_delete_workout_exercise_entry(self):
        #Arrange
        self.client.force_login(self.user)
        
        #Act
        response = self.client.delete(f'/api/exercises/{self.workout_exercise.pk}/')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WorkoutExercise.objects.count(), 0)

        #Check DB
        self.assertRaises(WorkoutExercise.DoesNotExist, lambda: WorkoutExercise.objects.get(pk=self.workout_exercise.pk))
        
    def test_create_set_entry_for_workout_exercise(self):
        #Arrange
        self.client.force_login(self.user)
        
        #Act
        response = self.client.post('/api/sets/', self.set_dto, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Set.objects.count(), 2)
        
        #Check DB
        set = Set.objects.get(order=1)
        self.assertEqual(set.workout_exercise.pk, self.set_dto[0]['workout_exercise'])
        self.assertEqual(set.weight, self.set_dto[0]['weight'])
        self.assertEqual(set.reps, self.set_dto[0]['reps'])
        
    def test_create_multiple_set_entries_for_workout_exercise(self):
        #Arrange
        self.client.force_login(self.user)
        multiple_sets = [
            {
                'weight': 40,
                'reps': 9,
                'workout_exercise': self.workout_exercise.pk,
                'order' : 1
            },
            {
                'weight':30,
                'reps':6,
                'workout_exercise':self.workout_exercise.pk,
                'order': 2
            }
        ]
        
        #Act
        response = self.client.post('/api/sets/', multiple_sets, format='json')

        #Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Set.objects.count(), 3)

        #Check DB
        set1 = Set.objects.get(order=1)
        set2 = Set.objects.get(order=2)
        self.assertEqual(set1.workout_exercise.pk, multiple_sets[0]['workout_exercise'])
        self.assertEqual(set2.workout_exercise.pk, multiple_sets[1]['workout_exercise'])
        self.assertEqual(set1.weight, multiple_sets[0]['weight'])
        self.assertEqual(set2.weight, multiple_sets[1]['weight'])
        
    def test_create_set_entry_for_workout_exercise_by_unauthenticated_user(self):
        #Act
        response = self.client.post('/api/sets/', self.set_dto, format='json')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Set.objects.count(), 1)
        
        #Check DB
        self.assertRaises(Set.DoesNotExist, lambda:Set.objects.get(order=1))
    
    def test_delete_set_entry(self):
        #Arrange
        self.client.force_login(self.user)

        #Act
        response = self.client.delete(f'/api/sets/{self.set.pk}/')
        
        #Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Set.objects.count(), 0)

        #Check DB
        self.assertRaises(Set.DoesNotExist, lambda: Set.objects.get(order=0))
