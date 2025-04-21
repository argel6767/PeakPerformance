from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MuscleViewSet, MovementViewSet

'''
different router must be used in order to have different endpoint pathing
otherwise for muscle will be 'movement/muscle' and movement will be 'movement/movement'
'''
muscle_router = DefaultRouter()
muscle_router.register('', MuscleViewSet)
movement_router = DefaultRouter()
movement_router.register('', MovementViewSet)
muscle_patterns = [path('', include(muscle_router.urls)),]
movement_patterns = [path('', include(movement_router.urls)),]
