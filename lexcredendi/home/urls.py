from django.urls import path
from . import views

app_name = "home_api"

urlpatterns = [
    path("seasonal-info/", views.seasonal_info, name="seasonal_info"),
]
