from django.http import JsonResponse
from django.db.models import Value, CharField
from django.db.models.functions import Replace, Lower
from .models import Record
from django.conf import settings


def serialize_art_record(record, request):
    """Helper function to serialize an Art Record object to a dictionary."""
    image_url = None
    if record.image:
        image_url = request.build_absolute_uri(record.image.url)

    return {
        "id": record.id,
        "album": record.album,
        "image_url": image_url,
    }


def serialize_album(album_data):
    """Helper function to serialize album data."""
    return {"code": album_data["album_code"], "title": album_data["album_title"]}


def list_albums(request):
    """
    API endpoint to list all unique albums.
    Returns a list of album objects, each with a 'code' and 'title'.
    """

    albums_query = (
        Record.objects.values_list("album", flat=True).distinct().order_by("album")
    )

    albums_data = []
    for album_name in albums_query:
        album_title = album_name.replace("_", " ").title()
        albums_data.append({"album_code": album_name, "album_title": album_title})

    serialized_albums = [serialize_album(album) for album in albums_data]
    return JsonResponse(serialized_albums, safe=False)


def album_images(request, album_code):
    """
    API endpoint to list all images for a specific album.
    Takes an 'album_code' (the album name) from the URL.
    """
    records = Record.objects.filter(album=album_code).order_by(
        "id"
    )  # Or 'order' if you add it
    if not records.exists():
        return JsonResponse(
            {"error": "Album not found or no images in album"}, status=404
        )

    data = [serialize_art_record(record, request) for record in records]
    return JsonResponse(data, safe=False)
