from django.urls import path
from . import views

app_name = "litcal_api"

urlpatterns = [
    path("today/", views.get_liturgical_day_info, name="get_liturgical_day_info"),
]
