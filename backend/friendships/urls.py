from django.urls import path
from .views import *

url_patterns = [
    path('/send-request/', SendFriendRequestView.asView(), name='send-request'),
    path('/accept-request/', AcceptFriendRequestView.asView(), name='accept-request'),
    path('reject/request/', RejectFriendRequestView.asView(), name='reject-request'),
    path('', GetAllStatusTypesRelationsView.asView(), name='get-all-relations-by-type'),
    path('/un-friend', UnFriendUserViews.asView(), name='unfriend-user')
]