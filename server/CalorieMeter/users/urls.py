from django.urls import path
from . import views
from .first_login import views as first_login_views

app_name = "users"

urlpatterns = [
    path("", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    # path("profile/update/", views.profile_update, name="profile_update"),
    path("first_login/check/", first_login_views.check, name="first_login"),
    path("first_login/form/" , first_login_views.form , name= "users_first_login_form" ),
    path("mypage/", views.mypage, name="mypage"),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_view, name="login"),
]