from django.shortcuts import render
from django.http import HttpResponse
from core.models import Meal

# Create your views here.
def meal_info(request, meal_id):
    try:
        meal = Meal.objects.get(id=meal_id)
    except Meal.DoesNotExist:
        return HttpResponse(status=404)

    target_calorie = 2000
    calorie_percentage = (meal.calorie / target_calorie) * 100

    if calorie_percentage > 100:
        calorie_percentage = 100
    elif calorie_percentage < 0:
        calorie_percentage = 0

    if meal.memo:
        memo = meal.memo
    else:
        memo = 'なし'
    
    data = {
        'meal': meal,
        'calorie_percentage': calorie_percentage,
        'target_calorie': target_calorie,
        'memo': memo,
    }

    return render(request, 'meal-info.html', data)