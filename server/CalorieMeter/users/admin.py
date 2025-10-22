from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser , Profile


@admin.register(CustomUser)
class CustomUsersAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ( "users_username", "user_email" , "is_staff", "date_joined" )
    search_fields = ("user_username", "user_email")
    ordering = ("user_joined")
    fieldsets =(
        (None, {"fields": ("user_email", "password")}),
        ("Profile", {"fields": ("user_username", "bio", "avatar")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("date_joined",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("user_email", "user_username", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "daily_kcal", "height_cm", "weight_kg", "created_at", "avatar")
    list_select_related = ("user",)