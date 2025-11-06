from django.db import models
from django.conf import settings
import enum
from datetime import date
import calendar

class TimeEaten(models.TextChoices):
    breakfast = "朝食"
    lunch = "昼食"
    dinner = "夕食"
    snack = "間食"
    other = "その他"

class MealManager(models.Manager):
    def get_meals_by_month(self, year, month):
        start_date = date(year, month, 1)
        last_day = calendar.monthrange(year, month)[1]
        end_date = date(year, month, last_day)
        return self.filter(date_eaten__range=[start_date, end_date])

    def get_total_calories_by_day(self, day, user):
        return self.filter(date_eaten=day, uploaded_by=user).aggregate(total_calories=models.Sum('calorie'))['total_calories']

    def get_total_amount_of_times_eaten(self, user):
        return self.filter(uploaded_by=user).aggregate(total_amount=models.Count('id'))['total_amount']

# 時間をユーザーが入力できるようにするのもあり
# Create your models here.
class Meal(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_eaten = models.DateField(null=True, blank=True)
    time_eaten = models.CharField(max_length=255, choices=TimeEaten.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='meals/')
    memo = models.TextField(null=True, blank=True)
# 栄養素
    calorie = models.IntegerField()
    
    # 後々追加する予定のデータ
    # protein = models.IntegerField()
    # fat = models.IntegerField()
    # carbohydrate = models.IntegerField()
    
    objects = MealManager()

    def __str__(self):
        return self.uploaded_by.email + " - " + self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            't_date': self.date_eaten.isoformat(),
            't_time': self.time_eaten,
            'imageUrl': self.image.url if self.image else None,
            'memo': self.memo,
            'calories': self.calorie,
        }
    

class DishManager(models.Manager):
    def get_meals_by_dish(self, dish, user):
        return Meal.objects.get(id=dish, user=user)

class Dish(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meals = models.ManyToManyField(Meal, related_name='dishes')
    date_eaten = models.DateField(null=True, blank=True)
    time_eaten = models.CharField(max_length=255, choices=TimeEaten.choices, null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_meals(self):
        print(self.meals.all())
        return self.meals.all()

    objects = DishManager()

    def __str__(self):
        return self.user.email + " - " + self.date_eaten.isoformat()