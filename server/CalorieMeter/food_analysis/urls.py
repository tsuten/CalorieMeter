from django.urls import path
from . import views

app_name = 'food_analysis'

urlpatterns = [
    # path('<int:record_id>/', views.record_detail, name='record_detail'),
    path('<int:record_id>/', views.analyze_record, name='analyze_record'),
]
