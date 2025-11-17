from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Meal
from datetime import date
# Create your views here.
@login_required
def calendar_view(request):
    return render(request, 'calendar.html')

def calendar_by_day_view(request, year, month, day):
    meals = Meal.objects.filter(date_eaten=date(year, month, day))
    return render(request, 'calendar_by_day.html', {'meals': meals})

def calendar_by_week_view(request, year, month, week):
    return render(request, 'calendar_by_week.html')

def calendar_by_month_view(request, year, month):
    
    meals = Meal.objects.get_meals_by_month(year, month)
    meals_list = []
    for meal in meals:
        meals_list.append(meal.to_dict())
    data = {"meals": meals_list}
    return render(request, 'calendar_by_month.html', {"data": data})