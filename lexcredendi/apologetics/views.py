from django.http import JsonResponse
from .models import Record
from home.bible import Bible


def serialize_record(record, linkify_text=True):
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
