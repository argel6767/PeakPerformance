from datetime import timedelta, date
from django.db import models
from movement.models import Movement
from users.models import CustomUser

# Create your models here.
'''
Models for workouts; broken down into WorkoutExercises and Sets
'''
class Workout(models.Model):
    user = models.ForeignKey(CustomUser, related_name="workouts", on_delete=models.CASCADE)
    duration = models.DurationField(default=timedelta) #duration of workout
    date = models.DateField(default=date.today)
    
    # static method for creating Workout entries
    @staticmethod
    def createWorkoutEntry(email: str, workout_dto) -> 'Workout':
        user = CustomUser.objects.get(email=email)
        
        # Start with required fields
        create_kwargs = {'user': user}
        
        # Add optional fields only if they're not None
        duration = workout_dto.validated_data.get('duration', None)
        if duration is not None:
            create_kwargs['duration'] = duration
            
        date = workout_dto.validated_data.get('date', None)
        if date is not None:
            create_kwargs['date'] = date
        
        # Create and return the workout with only the non-None fields
        return Workout.objects.create(**create_kwargs)
    
    def __str__(self):
        return f"{self.user.first_name}'s workout on {self.date}, lasted for {self.duration}"
    
    class Meta:
        ordering = ['date']


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, related_name='exercises', on_delete=models.CASCADE)
    movement = models.ForeignKey(Movement, related_name='movement', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    
    #bulk creates all workout exercises of one Workout
    @staticmethod
    def createWorkoutExerciseEntries(workout_exercises_dto) -> list['WorkoutExercise']:
        workouts_exercises = []
        
        for exercise_data in workout_exercises_dto.validated_data:
            exercise = WorkoutExercise(workout=exercise_data['workout'], movement=exercise_data['movement'], order=exercise_data['order'])
            workouts_exercises.append(exercise)
        
        return WorkoutExercise.objects.bulk_create(workouts_exercises)
    
    def __str__(self):
        return f'{self.movement.name} during workout: {self.workout}'
    
    class Meta:
        ordering = ['workout', 'order']

class Set(models.Model):
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    reps = models.PositiveIntegerField(default=0)
    workout_exercise = models.ForeignKey(WorkoutExercise, related_name='sets', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    
    # Bulk creates all Sets of a WorkoutExercise
    @staticmethod
    def createSetEntries(sets_dto) -> list['Set']:
        sets = []
        
        for set_data in sets_dto.validated_data:
            set = Set(weight=set_data['weight'], reps=set_data['reps'], workout_exercise=set_data['workout_exercise'], order=set_data['order'])
            sets.append(set)
        
        return Set.objects.bulk_create(sets)

    
    def __str__(self):
        return f'{self.weight} lbs for {self.reps} during exercise: {self.workout_exercise}'
    
    class Meta:
        ordering = ['workout_exercise', 'order']