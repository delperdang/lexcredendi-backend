import re
import requests
from bs4 import BeautifulSoup


class Podcast(object):
    """
    Captures the associated podcast data for a target record
    """

    def __init__(self, podcast_name):
        self.rss_feed = "https://feeds.fireside.fm/{}/rss".format(podcast_name)

    def _get_page_soup(self, url, parser="html.parser"):
        """
        retrieves web page soup for analysis
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features=parser)
        return soup

    def _extract_audio_url(self, soup, record):
        """Extracts audio url for target date mp3, returns URL string or None."""
        url = ""
        day_code = re.sub(r"^DAY0+(?=\d)", "DAY", record.code)
        items = soup.findAll("item")
        for item in items:
            title_text = item.title.text
            title_day_code = title_text.upper().replace(" ", "").split(":")[0]
            if day_code == title_day_code:
                url = item.enclosure.get("url")
                break
        return url if url else None

    def update_record(self, record):
        """
        returns an updated record object with podcast data (old method)
        """
        audio_soup = self._get_page_soup(self.rss_feed)
        audio_url = self._extract_audio_url(audio_soup, record)
        if audio_url:
            audio_link = '<br><a href="{}">{}</a>'.format(audio_url, "Click to play")
            record.text += audio_link
        return record
