from .models import Workout, WorkoutExercise, Set
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

class WorkoutDtoSerializer(ModelSerializer):
    date = serializers.DateField(required=False)
    duration = serializers.DurationField(required=False)

    class Meta:
        model = Workout
        fields = '__all__'

class WorkoutExerciseDtoSerializer(ModelSerializer):

    class Meta:
        model = WorkoutExercise
        fields = '__all__'

class SetDtoSerializer(ModelSerializer):
    
    class Meta:
        model = Set
        fields = '__all__'