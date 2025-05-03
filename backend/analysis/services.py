from users.models import CustomUser
from .serializers import *
from workout.models import WorkoutExercise, Workout
from movement.models import Movement
from datetime import datetime, timedelta
from .analysis import *
from .errors import *


def get_progressive_overload_rate(movement_id: int, weeks_ago: int, user: CustomUser) -> ProgressOverloadRateDtoSerializer:
    # Helper functions defined at the top
    def get_movement_or_raise(movement_id):
        movement = Movement.objects.filter(id=movement_id).first()
        if not movement:
            raise NoMovementEntryFoundError(f'No movement found with id: {movement_id}')
        return movement
    
    def find_relevant_workouts(date_start, date_end, fallback_strategy=None):
        # Get workouts in date range
        workouts = Workout.objects.filter(
            date__range=[date_start, date_end],
            exercises__movement=movement,
            user=user
        ).distinct()
        
        # Apply fallback strategy if no workouts found
        if len(workouts) == 0 and fallback_strategy:
            workouts = fallback_strategy()
            
        return workouts
    
    def get_recent_workouts_fallback():
        # Look for most recent workout with this movement
        try:
            most_recent = Workout.objects.filter(
                exercises__movement=movement, 
                user=user
            ).latest('date')
            return [most_recent]
        except Workout.DoesNotExist:
            raise NoExerciseEntryFoundError(f'No exercise found with movement {movement.name}')
    
    def get_baseline_workouts_fallback():
        # Find most recent workouts before baseline date
        workouts = Workout.objects.filter(
            date__lt=baseline_date,
            exercises__movement=movement,
            user=user
        ).order_by('-date').distinct()
        
        if len(workouts) == 0:
            raise InvalidDateRangeError(
                f"No workout with {movement.name} done {weeks_ago} or more weeks ago. Try a smaller range"
            )
        return workouts
    
    def calculate_volume_for_workouts(workouts):
        total_volume = 0
        for workout in workouts:
            exercises = WorkoutExercise.objects.filter(workout=workout, movement=movement)
            for exercise in exercises:
                sets = exercise.sets.all()
                total_volume += calculate_total_weight_volume(sets)
        return total_volume
    
    movement = get_movement_or_raise(movement_id)
    
    # Calculate date ranges
    today = datetime.now().date()
    baseline_date = today - timedelta(weeks=weeks_ago)
    
    # Get and process recent workouts
    recent_workouts = find_relevant_workouts(
        today - timedelta(days=7), 
        today,
        fallback_strategy=get_recent_workouts_fallback
    )
    recent_volume = calculate_volume_for_workouts(recent_workouts)
    
    # Get and process baseline workouts
    baseline_workouts = find_relevant_workouts(
        baseline_date - timedelta(days=7),
        baseline_date,
        fallback_strategy=get_baseline_workouts_fallback
    )
    baseline_volume = calculate_volume_for_workouts(baseline_workouts)
    
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

    # gets all of the WorkoutExercises with the movement specified was done by the user, then finds the total weight volume
    # for each one divided by 1000 (for ease of plotting)
    # the range is determined by the current date - 'num_of_weeks_back' for movements if no value is given then all instances are fetched
ALL_AVAILABLE_HISTORY = -1
def get_movement_progress_points(movement_id: int, user: CustomUser, num_of_weeks_back: int = ALL_AVAILABLE_HISTORY) -> dict:
    # Get the movement
    movement = Movement.objects.filter(id=movement_id).first()
    if not movement:
        raise NoMovementEntryFoundError(f'No movement found with id: {movement_id}')
    
    if num_of_weeks_back < -1:
        raise ValueError('number of weeks cannot be negative!')
    
    # Calculate date range if specified
    today = datetime.now().date()
    if num_of_weeks_back > 0:
        start_date = today - timedelta(weeks=num_of_weeks_back)
        workouts = Workout.objects.filter(
            date__range=[start_date, today],
            exercises__movement=movement,
            user=user
        ).distinct()
    else:
        # Get all workouts if no time range specified
        workouts = Workout.objects.filter(
            exercises__movement=movement,
            user=user
        ).distinct()
    
    if len(workouts) == 0:
        raise NoExerciseEntryFoundError(f'No workouts found with movement {movement.name}')
    
    # Sort workouts by date
    workouts = workouts.order_by('date')
    
    # Calculate total volume for each workout
    progress_points = []
    for workout in workouts:
        exercises = WorkoutExercise.objects.filter(workout=workout, movement=movement)
        total_volume = 0
        for exercise in exercises:
            sets = exercise.sets.all()
            if len(sets) == 0:  # Skip exercises with no sets
                continue
            total_volume += calculate_total_weight_volume(sets)
        
        # Only add to progress data if there was at least one exercise with sets
        if total_volume > 0:
            # Add the workout date and volume (divided by 1000) to the progress data
            progress_points.append({
                'date': workout.date,
                'volume': total_volume / 1000
            })
    
    if len(progress_points) == 0:
        raise NoSetEntriesFoundError(f'No sets found for movement {movement.name} in the specified time period')
    
    return {
        'movement': movement,
        'progress_points': progress_points
    }
    