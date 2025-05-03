from .views import *
from . import views
from django.urls import path


urlpatterns = [
    path('progressive-overload/', views.get_progressive_overload, name='get-progressive-overload'),
    path('orm/<int:movement_id>/', views.get_orm, name='get-one-rep-max'),
    path('relative-strength/<int:movement_id>/', views.get_relative_strength, name='get-relative-strength'),
    path('movement-progress/', views.get_movement_progress, name='get-movement-progress')
]
