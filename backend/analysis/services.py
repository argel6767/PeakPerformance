from users.models import CustomUser
from .serializers import *
from workout.models import WorkoutExercise, Workout
from movement.models import Movement
from datetime import datetime, timedelta
from .analysis import *
from .errors import *


def get_progressive_overload_rate(movement_id: int, weeks_ago: int, user: CustomUser) -> ProgressOverloadRateDtoSerializer:
    # Get the movement
    movement = Movement.objects.filter(id=movement_id).first()
    if not movement:
        raise NoMovementEntryFoundError(f'No movement found with id: {movement_id}')
    
    # Calculate date ranges
    today = datetime.now().date()
    baseline_date = today - timedelta(weeks=weeks_ago)
    
    # Get workouts for the movement in the most recent week
    recent_workouts = Workout.objects.filter(
        date__range=[today - timedelta(days=7), today],
        exercises__movement=movement,
        user=user
    ).distinct()
    
    if len(recent_workouts) == 0: # movement not done that past week
        #look for the last time they did it
        most_recent_workout = Workout.objects.filter(
            exercises__movement = movement, user=user).latest('date'),
        recent_workouts = [most_recent_workout]
    
    if len(recent_workouts) == 0: # movement never done before
        raise NoExerciseEntryFoundError(f'No exercise found with movement {movement.name}')
    
    # Calculate total volume for most recent week
    recent_volume = 0
    for workout in recent_workouts:
        exercises = WorkoutExercise.objects.filter(workout=workout, movement=movement)
        for exercise in exercises:
            sets = exercise.sets.all()
            recent_volume += calculate_total_weight_volume(sets)
    
    # Get workouts for the movement in the baseline week
    baseline_workouts = Workout.objects.filter(
        date__range=[baseline_date - timedelta(days=7), baseline_date],
        exercises__movement=movement,
        user=user
    ).distinct()
    
    if len(baseline_workouts) == 0: #no workout with movement done in baseline_weeks_ago
        # find the most recent that happened before baseline
        baseline_workouts = Workout.objects.filter(
            date__lt=baseline_date,
            exercises__movement=movement,
            user=user
        ).order_by('-date').distinct()
        
    if len(baseline_workouts) == 0:
        raise InvalidDateRangeError(f"No workout with {movement.name} done {weeks_ago} or more weeks ago. Try a smaller range")
    
    # Calculate total volume for baseline week
    baseline_volume = 0
    for workout in baseline_workouts:
        exercises = WorkoutExercise.objects.filter(workout=workout, movement=movement)
        for exercise in exercises:
            sets = exercise.sets.all()
            baseline_volume += calculate_total_weight_volume(sets)
    
    # Calculate progressive overload rate
    overload_rate = calculate_progress_overload_rate(baseline_volume, recent_volume)
    
    # Create and return the DTO
    return ProgressOverloadRateDtoSerializer({
        'movement': movement,
        'baseline_week_volume': baseline_volume,
        'most_recent_week_volume': recent_volume,
        'progressive_overload_change': overload_rate,
        'week_difference': weeks_ago
    })

def get_one_rep_max_for_movement(movement_id: int, user) -> EstimatedOneRepMaxDtoSerializer:
    # Get movement
    movement = Movement.objects.filter(id=movement_id).first()
    if not movement:
        raise NoMovementEntryFoundError(f'No movement found with id: {movement_id}')

    # Get most recent workout with movement done
    exercise = WorkoutExercise.objects.filter(
        movement=movement, 
        workout__user=user  # Changed from workout__user_id to workout__user
    ).select_related('workout').prefetch_related('sets').order_by('-workout__date').first()
    
    if not exercise:
        raise NoExerciseEntryFoundError(f"No WorkoutExercise done with movement {movement.name}")

    sets = exercise.sets.all()
    if len(sets) == 0:
        raise NoSetEntriesFoundError(f"No sets attached to WorkoutExercise: {exercise.pk}")
    
    largest_total_volume = 0
    max_set = None
    
    # Find highest performing set in exercise to use as `top set`
    for set in sets:
        volume = calculate_total_weight_volume([set])
        if volume > largest_total_volume:
            largest_total_volume = volume
            max_set = set

    one_rep_max = calculate_epley_formula(max_set)
    
    return EstimatedOneRepMaxDtoSerializer({
        'movement': movement,
        'estimated_orm': one_rep_max
    })