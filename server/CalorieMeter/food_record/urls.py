from django.urls import path
from . import views

app_name = 'food_record'

urlpatterns = [
    path('list', views.record_list, name='meal_info'),
    path('upload', views.record_create, name='record_create'),
    path('<int:record_id>/', views.record_detail, name='detail'), # food_analysisに移動予定
    # path('', views., name=''),
]