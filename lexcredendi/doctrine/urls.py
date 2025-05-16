from django.urls import path
from . import views

app_name = "doctrine_api"

urlpatterns = [
    path("", views.list_records, name="list_records"),
]
