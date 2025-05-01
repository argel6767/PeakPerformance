from django.db import models
from workout.models import Movement

# Create your models here.

# This class will be used as the dto to return the user's progress_overload_rate
# of a specific movement
class ProgressOverloadRateDto():

    def __init__(self, movement: Movement, baseline_week_volume: float, most_recent_week_volume:float, progress_overload_change: float, week_difference: int) -> None:
        self.movement = movement
        self.baseline_week_volume = baseline_week_volume
        self.most_recent_week_volume = most_recent_week_volume
        self.progressive_overload_change = progress_overload_change
        self.week_difference = week_difference

# This class will be used as the dto to return the user's estimated one rep max
# of a specific movement

class EstimatedOneRepMaxDto():

    def __init__(self, movement: Movement, estimated_orm: float) -> None:
        self.movement = movement
        self.estimated_orm = estimated_orm

# This class will be used as the dto to return a user's relative strength
class RelativeStrengthDto():
    
    def __init__(self, estimated_orm: float, user_weight: float, relative_strength: float) -> None:
        self.estimated_orm = estimated_orm
        self.user_weight = user_weight
        self.relative_strength = relative_strength