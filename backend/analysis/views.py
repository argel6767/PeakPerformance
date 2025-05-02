from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services import *
from .errors import *
from rest_framework.response import Response

# Create your views here.
# get progress_overload endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_progressive_overload(request):
    try:
        user = request.user
        movement_id = int(request.query_params.get('movement_id'))
        weeks_ago = int(request.query_params.get('weeks_ago'))
        result = get_progressive_overload_rate(movement_id=movement_id, weeks_ago=weeks_ago, user=user)
        return Response(result.data, status=status.HTTP_200_OK)
    except (NoMovementEntryFoundError, NoExerciseEntryFoundError, InvalidDateRangeError) as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except (ValueError, TypeError) as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# get one rep max for movement endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orm(request, movement_id):
    try:
        user = request.user
        result = get_one_rep_max_for_movement(movement_id=movement_id, user=user)
        return Response(result.data, status=status.HTTP_200_OK)
    except (NoMovementEntryFoundError, NoExerciseEntryFoundError, NoSetEntriesFoundError) as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def test_view(request):
    return Response({"message": "Analysis app is working"})