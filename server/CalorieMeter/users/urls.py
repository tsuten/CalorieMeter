from django.urls import path
from . import views
from components import views as error_views
from .first_login import views as first_login_views

app_name = "users"

urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    # path("profile/update/", views.profile_update, name="profile_update"),
    path("first_login/check/", first_login_views.check, name="first_login_check"),
    path("first_login/form/", first_login_views.form, name="first_login_form"),
    # path("mypage/", first_login_views.form, name="mypage"), 
    path("mypage/", views.mypage, name="mypage"),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_view, name="login"),
    path("error/", error_views.error, name="error"),
]