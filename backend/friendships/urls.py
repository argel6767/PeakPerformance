from django.urls import path
from .views import SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, GetAllStatusTypesRelationsView, UnFriendUserView

urlpatterns = [
    path('send-request/', SendFriendRequestView.as_view(), name='send-request'),
    path('accept-request/', AcceptFriendRequestView.as_view(), name='accept-request'),
    path('reject-request/', RejectFriendRequestView.as_view(), name='reject-request'),
    path('', GetAllStatusTypesRelationsView.as_view(), name='get-all-relations-by-type'),
    path('un-friend', UnFriendUserView.as_view(), name='unfriend-user')
]