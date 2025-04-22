from .serializers import WorkoutDtoSerializer, WorkoutExerciseDtoSerializer, SetDtoSerializer
from .models import Workout, WorkoutExercise, Set
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class WorkoutAPIView(APIView):
    
    def post(self, request):
        serializer = WorkoutDtoSerializer(request.data)
        
        if (not serializer.is_Valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        workout = Workout.createWorkoutEntry(email=user, workout_dto=serializer)
        
        return Response({'success', workout}, status.HTTP_201_CREATED)

class WorkoutExerciseAPIView(APIView):
    
    def post(self, request):
        serializer = WorkoutExerciseDtoSerializer(request.data, many=True)
        
        if (not serializer.is_Valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        exercises = WorkoutExercise.createWorkoutExerciseEntries(workout_exercises_dto=serializer)
        
        return Response({'success', exercises}, status.HTTP_201_CREATED)
    
class SetAPIView(APIView):
    
    def post(self, request):
        serializer = SetDtoSerializer(request.data, many=True)
        
        if (not serializer.is_Valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        sets = Set.createSetEntries(sets_dto=serializer)

        return Response({'success', sets}, status=status.HTTP_201_CREATED)
