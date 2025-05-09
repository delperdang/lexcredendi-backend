from django.http import JsonResponse
from django.db.models import Q
from .models import Record
from .bible import Bible

APP_NAME = "apologetics"


def serialize_record(record, linkify_text=False):
    """Helper function to serialize a Record object to a dictionary."""
    text_content = record.text
    if linkify_text:
        bible_linker = Bible()
        text_content = bible_linker.linkify(record.text)

    return {
        "code": record.code,
        "title": record.title,
        "text": text_content,
    }


def list_records(request):
    records = Record.objects.all().order_by("code")
    data = [serialize_record(record) for record in records]
    return JsonResponse(data, safe=False)


def record_details(request, code):
    try:
        record = Record.objects.get(pk=code)
        data = serialize_record(record, linkify_text=True)
        return JsonResponse(data)
    except Record.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)


def search_records(request):
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse([], safe=False)

    records = Record.objects.filter(
        Q(code__icontains=query) | Q(title__icontains=query) | Q(text__icontains=query)
    ).order_by("code")
    data = [serialize_record(record) for record in records]
    return JsonResponse(data, safe=False)
