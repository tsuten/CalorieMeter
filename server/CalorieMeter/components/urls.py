from django.urls import path
from . import views
from food_record.views import record_create, record_list
from food_analysis.views import analyze_record

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', record_create, name='upload'),
    path('history', record_list, name='list'),
    # path('meal/<int:meal_id>', record_detail, name='meal_detail'), # mealは未実装
    # path('upload', views.UploadView.as_view(), name='upload'), # 一旦、投稿はデータから受け取る
    path('analyze/<int:record_id>', analyze_record, name='analyze'),
    
    path('calendar', views.calendar, name='calendar'),
    path('statistics', views.statistics, name='statistics'),
    path('profile', views.profile, name='profile'),

    # エラーページ
    path('error', views.error, name='error'),
]