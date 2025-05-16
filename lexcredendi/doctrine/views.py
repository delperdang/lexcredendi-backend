from django.http import JsonResponse
from .models import Record


def serialize_doctrine_record(record):
    """Helper function to serialize a Doctrine Record object."""
    return {
        "code": record.code,
        "title": record.title,
        "text": record.text,
    }


def list_records(request):
    """
    API endpoint to list all doctrinal formulae records.
    """
    records = Record.objects.all().order_by("code")
    data = [serialize_doctrine_record(record) for record in records]
    return JsonResponse(data, safe=False)
