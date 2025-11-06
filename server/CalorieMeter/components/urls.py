from django.urls import path
from .views import index, UploadView, calendar, statistics, profile

urlpatterns = [
    path('', index, name='index'),
    path('upload', UploadView.as_view(), name='upload'),
    path('calendar', calendar, name='calendar'),
    path('statistics', statistics, name='statistics'),
    path('profile', profile, name='profile'),
]