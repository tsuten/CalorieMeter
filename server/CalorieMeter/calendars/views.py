from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
# @login_required
def calendar_view(request):
    return render(request, 'calendar.html')

def calendar_by_day_view(request, year, month, day):
    return render(request, 'calendar_by_day.html')

def calendar_by_week_view(request, year, month, week):
    return render(request, 'calendar_by_week.html')

def calendar_by_month_view(request, year, month):
    return render(request, 'calendar_by_month.html')