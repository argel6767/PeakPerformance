from models import Set
from users.models import UserWeight

'''
This file contains functions for various workout and progress related calculations
'''

# Calculates the total volume of a WorkoutExercise using its sets
def calculate_total_weight_volume(sets: list[Set]) -> float:
    total_volume= 0
    for set in sets:
        total_volume += set.reps * set.weight
    return total_volume

# Calculates the Progressive Overload Rate between two weeks to determine progress
def calculate_progress_overload_rate(initial_total_volume:float, current_total_volume) -> float:
    return (current_total_volume - initial_total_volume)/initial_total_volume

EPLEY_CONSTANT = 0.0333

# Calculates Epley Formula, ie a user's estimated one rep max
def calculate_epley_formula(top_set:Set) -> float:
    weight = top_set.weight
    reps = top_set.reps
    return weight * (1 + (EPLEY_CONSTANT * reps))

# Calculates a users estimated relative strength based off their 1RM and Body weight
def calculate_relative_strength(one_rep_max:float, userWeight:UserWeight) -> float:
    return one_rep_max/userWeight