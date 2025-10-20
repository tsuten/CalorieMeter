from django.urls import path
from .views import index, upload, calendar, statistics

urlpatterns = [
    path('', index, name='index'),
    path('upload', upload, name='upload'),
    path('calendar', calendar, name='calendar'),
    path('statistics', statistics, name='statistics'),
]