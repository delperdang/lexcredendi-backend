import requests
from bs4 import BeautifulSoup


class Intentions(object):
    """
    captures the latest list of intentions from the holy Father by month from the usccb
    """

    USCCB_INTENTIONS = "http://www.usccb.org/prayer-and-worship/prayers-and-devotions/the-popes-monthly-intention.cfm"

    def _get_month(self, local_now):
        """
        returns the current day of week spelled out
        """
        month = local_now.date().strftime("%B")
        return month

    def _get_page_soup(self, url, parser="html.parser"):
        """
        retrieves web page soup for analysis
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features=parser)
        return soup

    def _assemble_intentions_dict(self, soup, month):
        """
        assembles readings dictionary from readings soup
        """
        intention = {"title": "This Month's Papal Intentions", "text": ""}
        month_heading = soup.find(text=month)
        if bool(month_heading):
            next_p = month_heading.parent.find_next_sibling("p")
            intention["text"] = next_p.text.replace("\n", ": ")
        else:
            intention = {}
        return intention

    def get_record(self, localtime):
        """
        returns a context json of the current liturgical date
        """
        month_string = self._get_month(localtime)
        intentions_soup = self._get_page_soup(self.USCCB_INTENTIONS)
        intentions_record = self._assemble_intentions_dict(
            soup=intentions_soup, month=month_string
        )
        return intentions_record
