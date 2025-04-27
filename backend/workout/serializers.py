from .models import Workout, WorkoutExercise, Set
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

class WorkoutDtoSerializer(ModelSerializer):
    date = serializers.DateField(required=False)
    duration = serializers.DurationField(required=False)

    class Meta:
        model = Workout
        fields = ['id', 'duration', 'date', 'user']  # Only include necessary fields
        read_only_fields = ['user']  # Mark user as read-only

class WorkoutExerciseDtoSerializer(ModelSerializer):

    class Meta:
        model = WorkoutExercise
        fields = ['id', 'workout', 'movement', 'order']

class SetDtoSerializer(ModelSerializer):
    
    class Meta:
        model = Set
        fields = ['id','weight', 'reps', 'workout_exercise', 'order']