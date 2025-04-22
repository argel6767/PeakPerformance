from .serializers import WorkoutDtoSerializer, WorkoutExerciseDtoSerializer, SetDtoSerializer
from .models import Workout, WorkoutExercise, Set
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

'''
CRUD API for Workout Model
'''
class WorkoutViewSet(ModelViewSet):
    serializer_class = WorkoutDtoSerializer
    
    def get_queryset(self):
        # Return only workouts belonging to the current user
        return Workout.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        
        if (not serializer.is_Valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        workout = Workout.createWorkoutEntry(email=user, workout_dto=serializer)
        
        return Response({'success', workout}, status.HTTP_201_CREATED)

'''
CRUD API for WorkoutExercise Model
'''
class WorkoutExerciseViewSet(ModelViewSet):
    serializer_class = WorkoutExerciseDtoSerializer
    
    def get_queryset(self):
        return WorkoutExercise.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        
        if (not serializer.is_Valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        exercises = WorkoutExercise.createWorkoutExerciseEntries(workout_exercises_dto=serializer)
        
        return Response({'success', exercises}, status.HTTP_201_CREATED)

'''
CRUD API for Set Model
'''
class SetViewSet(ModelViewSet):
    serializer_class = SetDtoSerializer
    
    def get_queryset(self):
        return Set.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        
        if (not serializer.is_Valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        sets = Set.createSetEntries(sets_dto=serializer)

        return Response({'success', sets}, status=status.HTTP_201_CREATED)
