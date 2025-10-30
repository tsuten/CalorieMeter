from django.urls import path
from .import views

app_name = "first_login"

ulrpatterns = [
    path("check/" , views.check , name="check" ),
    path("form/" , views.form , name= "form" ),
]

