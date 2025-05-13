from django.urls import path
from . import views

app_name = "art_api"

urlpatterns = [
    path("albums/", views.list_albums, name="list_albums"),
    path("albums/<str:album_code>/images/", views.album_images, name="album_images"),
]
