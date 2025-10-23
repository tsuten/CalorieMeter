from django.db import models
from django.conf import settings
import enum

class TimeEaten(models.TextChoices):
    breakfast = "朝食"
    lunch = "昼食"
    dinner = "夕食"
    snack = "間食"
    other = "その他"

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

    time_eaten = models.CharField(max_length=255, choices=TimeEaten.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uploaded_by.username + " - " + self.name