from django.db import models
from django.conf import settings
import enum

class timeEaten(enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"
    other = "other"

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

    datetime_eaten = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uploaded_by.username + " - " + self.name