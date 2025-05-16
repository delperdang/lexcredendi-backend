from django.http import JsonResponse
from django.utils import timezone
from .models import Record
from home.podcast import Podcast
from .catechism import Catechism


def serialize_catechism_record(
    record, highlight=False, include_podcast=True, linkify=True
):
    """Helper function to serialize a Catechism Record object."""
    text_content = record.text
    podcast_link_html = None

    if include_podcast:
        podcast_util = Podcast("catechisminayear")
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
        catechism_linker = Catechism()
        text_content = catechism_linker.linkify(record.text)

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
        serialize_catechism_record(record, highlight=(record.code == current_day_code))
        for record in records
    ]
    return JsonResponse(data, safe=False)
