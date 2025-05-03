from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services import *
from .errors import *
from users.errors import NoUserWeightEntriesFoundError
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

#get relative strength for movement endpoint
@api_view(['GET'])
@permission_classes({IsAuthenticated})
def get_relative_strength(request, movement_id):
    try:
        user = request.user
        result = get_relative_strength_for_movement(movement_id=movement_id, user=user)
        return Response(result.data, status=status.HTTP_200_OK)
    except (NoMovementEntryFoundError, NoExerciseEntryFoundError, NoSetEntriesFoundError, NoUserWeightEntriesFoundError) as e:
        return Response({'error':str(e)}, status=status.HTTP_404_NOT_FOUND)
    except (ValueError, TypeError) as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

# get a movement's progress by user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_movement_progress(request):
    try:
        user = request.user
        movement_id = int(request.query_params.get('movement_id'))
        num_of_weeks_back = request.query_params.get('num_of_weeks_back')
        
        if num_of_weeks_back:
            points = get_movement_progress_points(movement_id=movement_id, user=user, num_of_weeks_back=int(num_of_weeks_back))
            serialized_points = MovementProgressDtoSerializer(points)
            return Response(serialized_points.data, status=status.HTTP_200_OK)
        else: #no given weeks back, ie grab all of them
            points = get_movement_progress_points(movement_id=movement_id, user=user)
            serialized_points = MovementProgressDtoSerializer(points)
            return Response(serialized_points.data, status=status.HTTP_200_OK)
        
    except (NoMovementEntryFoundError, NoExerciseEntryFoundError, NoSetEntriesFoundError) as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except (ValueError, TypeError) as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)