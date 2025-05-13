import requests
import dateutil.parser as dparser
from dateutil.parser._parser import ParserError
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class Readings(object):
    """
    Captures the latest daily readings text and audio from the USCCB
    """

    USCCB_ROOT = "http://www.usccb.org"
    USCCB_READINGS = "http://www.usccb.org/bible/readings/{}.cfm"

    def _get_readings_url(self, local_now):
        """
        asembles readings url based on local time
        """
        month_day_string = "{:%m%d}".format(local_now)
        year_string = "{:%Y}".format(local_now)[2:]
        date_string = "{}{}".format(month_day_string, year_string)
        url = self.USCCB_READINGS.format(date_string)
        return url

    def _get_page_soup(self, url, parser="html.parser"):
        """
        retrieves web page soup for analysis
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features=parser)
        return soup

    def _assemble_readings_dict(self, soup):
        """
        assembles readings dictionary from readings soup
        """
        readings = []
        headings = soup.find_all("div", {"class": "content-header"})
        for heading in headings:
            if (
                "READING 1" in heading.text.upper()
                or "READING I" in heading.text.upper()
            ):
                if heading.a.get("href", "").startswith("http"):
                    temp_link = heading.a.get("href")
                elif heading.a.get("href", "").startswith("/"):
                    temp_link = self.USCCB_ROOT + heading.a.get("href")
                else:
                    temp_link = self.USCCB_ROOT + "/" + heading.a.get("href")
                temp_citation = heading.a.text
                temp_title = "Reading 1"
                temp_text = '<a href="{}">{}</a>'.format(temp_link, temp_citation)
                if len(temp_citation) > 1:
                    readings.append(
                        {
                            "title": temp_title,
                            "text": temp_text,
                        }
                    )
            if (
                "READING 2" in heading.text.upper()
                or "READING II" in heading.text.upper()
            ):
                if heading.a.get("href", "").startswith("http"):
                    temp_link = heading.a.get("href")
                elif heading.a.get("href", "").startswith("/"):
                    temp_link = self.USCCB_ROOT + heading.a.get("href")
                else:
                    temp_link = self.USCCB_ROOT + "/" + heading.a.get("href")
                temp_citation = heading.a.text
                temp_title = "Reading 2"
                temp_text = '<a href="{}">{}</a>'.format(temp_link, temp_citation)
                if len(temp_citation) > 1:
                    readings.append(
                        {
                            "title": temp_title,
                            "text": temp_text,
                        }
                    )
            if "RESPONSORIAL PSALM" in heading.text.upper():
                if heading.a.get("href", "").startswith("http"):
                    temp_link = heading.a.get("href")
                elif heading.a.get("href", "").startswith("/"):
                    temp_link = self.USCCB_ROOT + heading.a.get("href")
                else:
                    temp_link = self.USCCB_ROOT + "/" + heading.a.get("href")
                temp_citation = heading.a.text
                temp_title = "Responsorial Psalm"
                temp_text = '<a href="{}">{}</a>'.format(temp_link, temp_citation)
                if len(temp_citation) > 1:
                    readings.append(
                        {
                            "title": temp_title,
                            "text": temp_text,
                        }
                    )
            if "GOSPEL" in heading.text.upper():
                if heading.a.get("href", "").startswith("http"):
                    temp_link = heading.a.get("href")
                elif heading.a.get("href", "").startswith("/"):
                    temp_link = self.USCCB_ROOT + heading.a.get("href")
                else:
                    temp_link = self.USCCB_ROOT + "/" + heading.a.get("href")
                temp_citation = heading.a.text
                temp_title = "Gospel"
                temp_text = '<a href="{}">{}</a>'.format(temp_link, temp_citation)
                if len(temp_citation) > 1:
                    readings.append(
                        {
                            "title": temp_title,
                            "text": temp_text,
                        }
                    )
        return readings

    def _extract_audio(self, soup):
        """
        Extracts the podcast audio URL from the provided HTML snippet.

        Args:
            html_content (str): The HTML content as a string.

        Returns:
            str: The absolute URL of the podcast audio, or None if not found.
        """
        base_url = "https://bible.usccb.org"
        target_url = None

        link_tag = soup.find("a", class_="icon-microphone", string="LISTEN PODCAST")

        if link_tag and link_tag.has_attr("href"):
            relative_url = link_tag["href"]
            target_url = urljoin(base_url, relative_url)
        else:
            print("Could not find the target link tag or its href attribute.")

        audio = {
            "title": "Podcast Audio Link",
            "url": target_url,
            "text": (
                f'<a href="{target_url}">Click to listen</a>'
                if target_url
                else "Link not found"
            ),
        }
        return audio

    def get_records(self, localtime):
        """
        returns a context json of the current readings and audio
        """
        readings_url = self._get_readings_url(localtime)
        readings_soup = self._get_page_soup(readings_url)
        readings_records = self._assemble_readings_dict(readings_soup)
        audio_record = self._extract_audio(readings_soup)
        readings_records.append(audio_record)
        return readings_records
