from .models import Workout, WorkoutExercise, Set
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

class WorkoutDtoSerializer(ModelSerializer):
    date = serializers.DateField(required=False)
    duration = serializers.DurationField(required=False)

    class Meta:
        model = Workout
        fields = ['duration', 'date']

class WorkoutExerciseDtoSerializer(ModelSerializer):

    class Meta:
        model = WorkoutExercise
        fields = ['workout', 'movement', 'order']

class SetDtoSerializer(ModelSerializer):
    
    class Meta:
        model = Set
        fields = ['weight', 'reps', 'workout_exercise', 'order']