import os , uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

def user_avatar_path(instance , filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"avatars/users_{instance.user_id}/{uuid_uuid4().hex}{ext}"

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    daily_kcal = models.PositiveIntegerField(default=2000, help_text="1日の目標(kcal)")
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Profile({self.user.username})"

# ユーザー作成時に空のプロフィールを自動作成
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    # 既存ユーザーに対しても profile が無ければ作る
    if not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
