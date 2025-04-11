from datetime import timedelta
from django.utils import timezone
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
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.first_name}'s workout on {self.date} lasted for {self.duration}"
    
    class Meta:
        ordering = ['date']


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, related_name='exercises', on_delete=models.CASCADE)
    movement = models.ForeignKey(Movement, related_name='movement', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'{self.movement.name} during {self.workout}'
    
    class Meta:
        ordering = ['workout', 'order']

class Set(models.Model):
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    reps = models.PositiveIntegerField(default=0)
    workout_exercise = models.ForeignKey(WorkoutExercise, related_name='sets', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    
    def __str__(self):
        return f'{self.weight} lbs for {self.reps}'
    
    class Meta:
        ordering = ['workout_exercise', 'order']