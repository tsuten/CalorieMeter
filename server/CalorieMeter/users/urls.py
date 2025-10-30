
from django.urls import path
from . import views
from .first_login import views as first_login_views

urlpatterns = [
    path("", views.register, name="register"),
    # path("profile/", views.first_login, name="profile"),
    # path("profile/update/", views.profile_update, name="profile_update"),
    path("first_login/check/", first_login_views.check, name="first_login"),
    path("first_login/form/" , first_login_views.form , name= "form" ),
]