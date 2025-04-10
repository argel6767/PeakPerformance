from django.db import models

# Create your models here.
'''
Models for workouts; broken down into WorkoutExercises and Sets
'''

class Workout(models.Model):
    user = models.ForeignKey(CustomUser, related_name="user", on_delete=models.CASCADE)
    length = models.TimeField() #TODO fill in arguments

class WorkoutExercise(models.Model):
    movement = models.ForeignKey(Movement, related_name='movement', on_delete=models.CASCADE)
    

class Set(models.Model):
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    reps = models.PositiveIntegerField(default=0)
    workout_exercise = models.ForeignKey(WorkoutExercise, related_name='sets', on_delete=models.CASCADE)