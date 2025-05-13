from django.http import JsonResponse
from django.db.models import Q
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


def record_details(request, code):
    """
    API endpoint for details of a specific prayer.
    """
    try:
        record = Record.objects.get(pk=code)
        data = serialize_prayer_record(record)
        return JsonResponse(data)
    except Record.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)


def search_records(request):
    """
    API endpoint to search prayer records.
    Includes searching in Latin title and text.
    """
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse([], safe=False)

    records = (
        Record.objects.filter(
            Q(code__icontains=query)
            | Q(title__icontains=query)
            | Q(text__icontains=query)
            | Q(latin_title__icontains=query)
            | Q(latin_text__icontains=query)
        )
        .order_by("code")
        .distinct()
    )

    data = [serialize_prayer_record(record) for record in records]
    return JsonResponse(data, safe=False)
