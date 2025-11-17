from django.db import models
from food_record.models import FoodRecord

class FoodAnalysisResult(models.Model):
    record = models.OneToOneField(FoodRecord, on_delete=models.CASCADE, related_name='analysis')
    predicted_food = models.CharField(max_length=100)
    confidence = models.FloatField()
    nutrients = models.JSONField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for Record {self.record.record_id}"
