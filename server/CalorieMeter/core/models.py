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

# 時間をユーザーが入力できるようにするのもあり
# Create your models here.
class Meal(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='meals/')
    calorie = models.IntegerField()
    
    # 後々追加する予定のデータ
    # protein = models.IntegerField()
    # fat = models.IntegerField()
    # carbohydrate = models.IntegerField()

    date_eaten = models.DateField(null=True, blank=True)
    time_eaten = models.CharField(max_length=255, choices=TimeEaten.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MealManager()

    def __str__(self):
        return self.uploaded_by.user_email + " - " + self.name

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.name,
            'date': self.date_eaten.isoformat(),
            'imageUrl': self.image.url if self.image else None,
            'calories': self.calorie,
            'description': self.time_eaten
        }