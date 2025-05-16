from django.http import JsonResponse
from .models import Record


def serialize_prayer_record(record):
    """Helper function to serialize a Prayer Record object."""
    return {
        "code": record.code,
        "title": record.title,
        "text": record.text,
        "latin_title": (record.latin_title if record.latin_title else None),
        "latin_text": (record.latin_text if record.latin_text else None),
    }


def list_records(request):
    """
    API endpoint to list all prayer records.
    """
    records = Record.objects.all().order_by("code")
    data = [serialize_prayer_record(record) for record in records]
    return JsonResponse(data, safe=False)
