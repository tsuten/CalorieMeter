from django.urls import path
from . import views
from food_analysis.views import analyze_record

app_name = 'food_record'

urlpatterns = [
    path('list', views.record_list, name='meal_info'),
    path('upload', views.record_create, name='record_create'),
    # path('', views., name=''),
]