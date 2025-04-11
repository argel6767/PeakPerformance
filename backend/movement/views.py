from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from models import Muscle, Movement
from .permissions import IsAdminUser
from .serializers import MuscleSerializer, MovementSerializer

# Create your views here.
"""
API view to create a new muscle entry.
Only admin users can create new muscles.
"""
class MuscleViewSet(ModelViewSet):
    serializer_class = MuscleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Muscle.objects.all()

"""
API view to create a new movement entry.
Only admin users can create new movements.
"""
class MovementViewSet(ModelViewSet):
    serializer_class = MovementSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Movement.objects.all()