from django.urls import path
from . import views

app_name = 'food_analysis'

urlpatterns = [
    path('<int:id>/', views.analyze_record, name='analyze_record'),
]
