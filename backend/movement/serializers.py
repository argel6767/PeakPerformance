from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField

from .models import Muscle, Movement

class MuscleSerializer(ModelSerializer):
    class Meta:
        model = Muscle
        fields = '__all__'
        
class MovementSerializer(ModelSerializer):
    #finds the muscle entries in db to create entries in junction table
    muscles_worked = PrimaryKeyRelatedField(
        queryset=Muscle.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = Movement
        fields = '__all__'