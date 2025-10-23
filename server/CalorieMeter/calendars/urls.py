from django.urls import path
from .views import calendar_view, calendar_by_day_view, calendar_by_week_view, calendar_by_month_view

urlpatterns = [
    path('', calendar_view, name='calendar'),
    path('d/<int:year>/<int:month>/<int:day>/', calendar_by_day_view, name='calendar_by_day'),
    path('w/<int:year>/<int:month>/<int:week>/', calendar_by_week_view, name='calendar_by_week'),
    path('m/<int:year>/<int:month>/', calendar_by_month_view, name='calendar_by_month'),
]