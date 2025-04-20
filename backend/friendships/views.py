from users.models import CustomUser
from .serializers import FriendshipsSerializer, FriendRequestSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class SendFriendRequestView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Grab user doing request
            from_user = request.user
            # The recipient is fetched using the email from the serializer
            to_email = serializer.validated_data['email']
            to_user = CustomUser.objects.get(email=to_email)
            #check if user is trying to send a request to themselves
            if from_user == to_user:
                return Response({"error": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)
            pending = from_user.send_friend_request(to_user)
            return Response({"success": f"Friend request sent: {pending}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptFriendRequestView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            #Grab user doing request
            from_user = request.user
            # The recipient is fetched using the email from the serializer
            to_email = serializer.validated_data['email']
            to_user = CustomUser.objects.get(email=to_email)
            #check if user is trying to accept a request to themselves
            if from_user == to_user:
                return Response({"error": "You cannot accept a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)
            accepted = to_user.accept_friend_request(from_user=from_user)
            return Response({'success': f'Friend request accepted! {accepted}'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RejectFriendRequestView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            #Grab user doing request
            from_user = request.user
            # The recipient is fetched using the email from the serializer
            to_email = serializer.validated_data['email']
            original_requester = CustomUser.objects.get(email=to_email)
            
            #check if user is trying to reject a request to themselves
            if from_user == original_requester:
                return Response({"error": "You cannot reject a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)
            rejected = from_user.reject_friend_request(from_user=original_requester)

            return Response({'success': f'Friend request rejected! {rejected}'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Gets all a users status type, ie all pending, all accepted, deleted, blocked etc
'''
class GetAllStatusTypesRelationsView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        from_user = request.user
        status_type = request.query_params.get('status-type')
        if (status_type is None):
            return Response({'error': 'No status type given'}, status=status.HTTP_400_BAD_REQUEST)

        relations = from_user.get_all_users_of_status_type(status_type)
        
        serializer = FriendshipsSerializer(relations, many=True)
        return Response({'success': serializer.data}, status=status.HTTP_200_OK)

class UnFriendUserViews(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            #Grab user doing request
            from_user = request.user
            # The recipient is fetched using the email from the serializer
            to_email = serializer.validated_data['email']
            friend_user = CustomUser.objects.get(email=to_email)
            
            #check if user is trying to unfriend themselves
            if from_user == friend_user:
                return Response({"error": "You cannot unfriend yourself."}, status=status.HTTP_400_BAD_REQUEST)

            from_user.unfriend_user(friend_user)
            return Response({'success': f'User: {to_email}, successfully un-added!'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
