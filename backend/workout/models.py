from datetime import timedelta, date
from django.db import models
from movement.models import Movement, Muscle
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
    
    #Returns all data from workout, including the WorkoutExercises and their child sets, Movements done during each WorkoutExercise and Muscles Worked
    @staticmethod
    def get_workout_summary(user: CustomUser, workout_id):
        from .serializers import WorkoutDtoSerializer, WorkoutExerciseDtoSerializer, SetDtoSerializer #grab serializers to make json
        from movement.serializers import MovementSerializer, MuscleSerializer
    
        workout = Workout.objects.get(user=user, id=workout_id) ##Get Workout
        workout_data = WorkoutDtoSerializer(workout).data
        workout_summary = {'workout': workout_data}
        
        exercises = WorkoutExercise.objects.filter(workout=workout) #Get all exercises attached to workout
        
        for exercise in exercises: ##Grab info for each exercise
            exercise_data = WorkoutExerciseDtoSerializer(exercise).data
            
            movement = Movement.objects.get(pk=exercise_data['movement']) #Grab the movement done during the workout
            movement_data = MovementSerializer(movement).data
            
            muscles_pks = movement_data['muscles_worked'] #Grab the muscles worked with the movement done
            muscles = Muscle.objects.filter(id__in=muscles_pks)
            muscles_data = MuscleSerializer(muscles, many=True).data
            
            movement_data['muscles_worked'] = muscles_data #Map the data fetched, instead of just their pks
            exercise_data['movement'] = movement_data
            workout_summary[f'exercise {exercise.order}'] = exercise_data
            
            sets = Set.objects.filter(workout_exercise=exercise) #Grab sets of exercise
            workout_summary[f'sets for exercise {exercise.order}'] = SetDtoSerializer(sets, many=True).data
        
        return workout_summary

    
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