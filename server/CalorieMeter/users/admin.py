from django.contrib import admin
from .models import AuthAccount, UserProfile, OnboardingStatus

@admin.register(AuthAccount)
class AuthAccountAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "date_joined")
    search_fields = ("email",)
    ordering = ("-date_joined",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "auth",
        "display_name",
        "height_cm",
        "weight_kg",
        "daily_kcal",
        "created_at",
        "target_weight",
    )
    list_select_related = ("auth",)
    search_fields = ("auth__email", "display_name")
    ordering = ("-created_at",)


@admin.register(OnboardingStatus)
class OnboardingStatusAdmin(admin.ModelAdmin):
    list_display = ("user", "is_completed", "completed_at")
    list_select_related = ("user",)
    search_fields = ("user__email", "user__profile__display_name")
    ordering = ("-completed_at",)
