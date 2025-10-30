
from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.first_login, name="profile"),
    # path("profile/update/", views.profile_update, name="profile_update"),
]
