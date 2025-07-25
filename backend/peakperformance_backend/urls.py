"""
URL configuration for peakperformance_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from movement.urls import muscle_patterns, movement_patterns
from workout.urls import workout_patterns, workout_exercise_patterns, set_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/muscles/', include(muscle_patterns)),
    path('api/movements/', include(movement_patterns)),
    path('api/friends/', include('friendships.urls')),
    path('api/workouts/', include(workout_patterns)),
    path('api/exercises/', include(workout_exercise_patterns)),
    path('api/sets/', include(set_patterns)),
    path('api/analysis/', include('analysis.urls'))
]
