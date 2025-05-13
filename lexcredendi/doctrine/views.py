from django.http import JsonResponse
from django.db.models import Q
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


def record_details(request, code):
    """
    API endpoint for details of a specific doctrinal formula.
    """
    try:
        record = Record.objects.get(pk=code)
        data = serialize_doctrine_record(record)
        return JsonResponse(data)
    except Record.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)


def search_records(request):
    """
    API endpoint to search doctrinal formulae records.
    """
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse([], safe=False)

    records = Record.objects.filter(
        Q(code__icontains=query) | Q(title__icontains=query) | Q(text__icontains=query)
    ).order_by("code")

    data = [serialize_doctrine_record(record) for record in records]
    return JsonResponse(data, safe=False)
