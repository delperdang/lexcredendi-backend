from django.urls import path
from . import views

app_name = "bible_api"

urlpatterns = [
    path("", views.list_records, name="list_records"),
    path("details/<str:code>/", views.record_details, name="record_details"),
    path("search/", views.search_records, name="search_records"),
]
