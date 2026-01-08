from django.db import models
from food_record.models import FoodRecord

class FoodAnalysis(models.Model):
    record = models.OneToOneField(FoodRecord, on_delete=models.CASCADE, related_name='analysis')
    predicted_food_name = models.CharField(max_length=100, blank=True) # food_recordのdescriptionと関連付け
    confidence = models.FloatField() # 信頼度
    nutrients = models.JSONField() # 栄養素情報 food_recordのnutrientsと関連付け
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for Record {self.record.record_id}"