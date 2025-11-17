# Create your models here.
from django.db import models
from  users.models import UserProfile
from django.db import models
import os
import uuid

def food_image_upload_path(instance, filename):
    """
    食品画像の保存先
    保存パス: settings.MEDIA_ROOT/food_records/
    food_records_{user_id}/ランダムuuid.拡張子 というパスで保存
    """
    ext = (os.path.splitext(filename)[1] or ".bin").lower()
    return f"food_records/food_records_{instance.recorded_by.id}/{uuid.uuid4().hex}{ext}"

class FoodRecord(models.Model):
    """
    食品記録モデル。
    nutrients フィールドには、{"protein": 10.5, "fat": 5.2, "carbs": 20.1} のような
    栄養素名をキー、含有量（float）を値とする JSON データを格納します。
    """
    record_id = models.AutoField(primary_key=True)
    recorded_by = models.ForeignKey(
        UserProfile,
        to_field='id',             # ← user_idを外部キーに指定
        db_column='id',
        on_delete=models.CASCADE,
        related_name="food_records"
    )
    image = models.ImageField(
        upload_to=food_image_upload_path,
        blank=True,
        null=True,
        ) # MEDIA_ROOT 以下に保存
    description = models.TextField(blank=True, null=True)
    calories = models.FloatField(blank=True, null=True)
    nutrients = models.JSONField(blank=True, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        date_str = self.recorded_at.strftime('%Y-%m-%d') if self.recorded_at else 'N/A'
        return f"Record {self.record_id} (UserID: {self.recorded_by.id}) - {date_str}"