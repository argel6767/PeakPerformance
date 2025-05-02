from .views import *
from . import views
from django.urls import path


urlpatterns = [
    path('progressive-overload/', views.get_progressive_overload, name='get-progressive-overload'),
    path('orm/<int:movement_id>/', views.get_orm, name='get-orm')
]
