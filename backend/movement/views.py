from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Muscle, Movement
from .permissions import IsAdminUser
from .serializers import MuscleSerializer, MovementSerializer

# Create your views here.

"""
API view to create a new muscle entry.
Only admin users can create new muscles.
"""
class MuscleViewSet(ModelViewSet):
    serializer_class = MuscleSerializer
    queryset = Muscle.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

"""
API view to create a new movement entry.
Only admin users can create new movements.
"""
class MovementViewSet(ModelViewSet):
    serializer_class = MovementSerializer
    queryset = Movement.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]