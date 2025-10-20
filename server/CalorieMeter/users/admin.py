from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "daily_kcal", "height_cm", "weight_kg", "created_at", "avatar")
    search_fields = ("user_username", "user_email")
    list_select_related = ("user",)