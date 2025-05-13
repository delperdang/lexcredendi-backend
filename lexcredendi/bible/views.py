from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import Record
from .podcast import Podcast
from .bible import Bible


def serialize_bible_record(
    record, highlight=False, include_podcast=False, linkify=False
):
    """Helper function to serialize a Bible Record object."""
    text_content = record.text
    podcast_link_html = None

    if include_podcast:
        podcast_util = Podcast("bibleinayear")
        try:
            audio_soup = podcast_util._get_page_soup(podcast_util.rss_feed)
            podcast_url = podcast_util._extract_audio_url(audio_soup, record)
            if podcast_url:
                podcast_link_html = (
                    f'<br><a href="{podcast_url}">Click to play podcast</a>'
                )
        except Exception:
            podcast_link_html = None

    if linkify:
        bible_linker = Bible()
        text_content = bible_linker.linkify(record.text)

    return {
        "code": record.code,
        "title": record.title,
        "text": text_content,
        "highlight": highlight,
        "podcast_link_html": podcast_link_html,
    }


def list_records(request):
    records = Record.objects.all().order_by("code")
    current_day_code = "DAY" + timezone.localtime().date().strftime("%j")

    data = [
        serialize_bible_record(record, highlight=(record.code == current_day_code))
        for record in records
    ]
    return JsonResponse(data, safe=False)


def record_details(request, code):
    try:
        record = Record.objects.get(pk=code)
        data = serialize_bible_record(record, include_podcast=True, linkify=True)
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

    data = [serialize_bible_record(record, linkify=True) for record in records]
    return JsonResponse(data, safe=False)
