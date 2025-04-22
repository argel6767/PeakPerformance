from users.models import CustomUser
from .serializers import WorkoutDtoSerializer
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
        
    
