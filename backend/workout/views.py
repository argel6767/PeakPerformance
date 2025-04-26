from .serializers import WorkoutDtoSerializer, WorkoutExerciseDtoSerializer, SetDtoSerializer
from .models import Workout, WorkoutExercise, Set
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.

'''
CRUD API for Workout Model
'''
class WorkoutViewSet(ModelViewSet):
    serializer_class = WorkoutDtoSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        # Return only workouts belonging to the current user
        return Workout.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        
        if (not serializer.is_valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        workout = Workout.createWorkoutEntry(email=user.email, workout_dto=serializer)
        workout_serialized = self.get_serializer(instance=workout)
        
        return Response({'success': workout_serialized.data}, status=status.HTTP_201_CREATED)

'''
CRUD API for WorkoutExercise Model
'''
class WorkoutExerciseViewSet(ModelViewSet):
    serializer_class = WorkoutExerciseDtoSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        return WorkoutExercise.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        
        if (not serializer.is_valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        exercises = WorkoutExercise.createWorkoutExerciseEntries(workout_exercises_dto=serializer)
        exercises_serialized = self.get_serializer(instance=exercises, many=True)
        
        return Response({'success': exercises_serialized.data}, status.HTTP_201_CREATED)

'''
CRUD API for Set Model
'''
class SetViewSet(ModelViewSet):
    serializer_class = SetDtoSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        return Set.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        
        if (not serializer.is_valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        sets = Set.createSetEntries(sets_dto=serializer)
        sets_serialized = self.get_serializer(instance=sets, many=True)

        return Response({'success': sets_serialized.data}, status=status.HTTP_201_CREATED)
