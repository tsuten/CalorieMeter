from django.urls import path
from .views import index, UploadView, calendar, statistics, profile
from food_recognition.views import meal_info

urlpatterns = [
    path('', index, name='index'),
    path('upload', UploadView.as_view(), name='upload'),
    path('calendar', calendar, name='calendar'),
    path('statistics', statistics, name='statistics'),
    path('profile', profile, name='profile'),
    path('meal-info/<int:meal_id>', meal_info, name='meal-info'),
]