from datetime import datetime
from django.test import TestCase

from analysis.analysis import *
from users.models import UserWeight
from workout.models import Set

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