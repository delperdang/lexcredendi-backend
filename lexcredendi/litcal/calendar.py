import requests
from bs4 import BeautifulSoup


class Calendar(object):
    """
    Captures the latest liturgical calendar entry from the usccb readings
    """

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

    def _assemble_litcal_dict(self, soup):
        """
        assembles readings dictionary from readings soup
        """
        litcal = {"title": "", "text": ""}
        title = soup.find("meta", property="og:title")
        paragraphs = soup.find_all("p")
        for paragraph in paragraphs:
            if "Lectionary:" in paragraph.text:
                litcal["title"] = title.get("content", None)
                litcal["text"] = paragraph.text
        return litcal

    def get_record(self, localtime):
        """
        returns a context json of the current liturgical date
        """
        readings_url = self._get_readings_url(localtime)
        readings_soup = self._get_page_soup(readings_url)
        litcal_record = self._assemble_litcal_dict(readings_soup)
        return litcal_record
