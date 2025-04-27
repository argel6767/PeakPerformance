from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutViewSet, WorkoutExerciseViewSet, SetViewSet 

'''
Different routers are used to ensure each model has its own pathing
'''

workout_router = DefaultRouter()
workout_router.register('', WorkoutViewSet, basename='workout')

workout_exercise_router = DefaultRouter()
workout_exercise_router.register('', WorkoutExerciseViewSet, basename='workout-exercise')

set_router = DefaultRouter()
set_router.register('', SetViewSet, basename='set')

workout_patterns = workout_router.urls
workout_exercise_patterns = workout_exercise_router.urls
set_patterns = set_router.urls