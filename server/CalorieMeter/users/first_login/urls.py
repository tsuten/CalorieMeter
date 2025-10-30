from django.urls import path
from .import views

app_name = "first_login"

ulrpatterns = [
    path("cheak/" , views.cheak , name="cheak" ),
    path("form/" , views.form , name= "form" ),
]

