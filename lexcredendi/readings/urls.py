from django.urls import path
from . import views

app_name = "readings_api"

urlpatterns = [
    path("today/", views.get_daily_readings, name="get_daily_readings"),
]
