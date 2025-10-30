from django.urls import path
from . import views

app_name = "first_login"

urlpatterns = [
    path("check/" , views.check , name="check" ),
    path("form/" , views.form , name= "form" ),
]

