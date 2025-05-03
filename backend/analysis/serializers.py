from rest_framework import serializers
from workout.models import Movement
from movement.serializers import MovementSerializer

# This class will be used as the dto to return the user's progress_overload_rate
# of a specific movement
class ProgressOverloadRateDtoSerializer(serializers.Serializer):
    movement = MovementSerializer()
    baseline_week_volume = serializers.FloatField()
    most_recent_week_volume = serializers.FloatField()
    progressive_overload_change = serializers.FloatField()
    week_difference = serializers.IntegerField()

# This class will be used as the dto to return the user's estimated one rep max
# of a specific movement
class EstimatedOneRepMaxDtoSerializer(serializers.Serializer):
    movement = MovementSerializer()
    estimated_orm = serializers.FloatField()

# This class will be used as the dto to return a user's relative strength for a certain movement
class RelativeStrengthDtoSerializer(serializers.Serializer):
    movement = MovementSerializer()
    estimated_orm = serializers.FloatField()
    user_weight = serializers.FloatField()
    relative_strength = serializers.FloatField()

# This class is the serializer for an actual point (date, progress)
class MovementProgressPointSerializer(serializers.Serializer):
    date = serializers.DateField()
    volume = serializers.FloatField()

# This class will be used as the dto to return a list of movement progress points
class MovementProgressDtoSerializer(serializers.Serializer):
    movement = MovementSerializer()
    progress_points = MovementProgressPointSerializer(many=True)