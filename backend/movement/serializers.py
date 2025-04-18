from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField

from .models import Muscle, Movement

class MuscleSerializer(ModelSerializer):
    class Meta:
        model = Muscle
        fields = ('name', 'category')
        
class MovementSerializer(ModelSerializer):
    #finds the muscle entries in db to create entries in junction table
    muscles_worked = PrimaryKeyRelatedField(
        queryset=Muscle.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = Movement
        fields = ['name', 'muscles_worked', 'type', 'movement_image_url']