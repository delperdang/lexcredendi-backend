from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from dateutil.relativedelta import SU


class Mysteries(object):
    """
    Determines the appropriate mysteries of the Rosary for the given day and season
    """

    JOYFUL = {
        "title": "Today's Mysteries of the Rosary",
        "text": '<a href="https://www.usccb.org/prayers/rosary-life-joyful-mysteries">Joyful Mysteries</a>',
    }
    SORROWFUL = {
        "title": "Today's Mysteries of the Rosary",
        "text": '<a href="https://www.usccb.org/prayers/rosary-life-sorrowful-mysteries">Sorrowful Mysteries</a>',
    }
    GLORIOUS = {
        "title": "Today's Mysteries of the Rosary",
        "text": '<a href="https://www.usccb.org/prayers/rosary-life-glorious-mysteries">Glorious Mysteries</a>',
    }
    LUMINOUS = {
        "title": "Today's Mysteries of the Rosary",
        "text": '<a href="https://www.usccb.org/prayers/rosary-life-luminous-mysteries">Luminous Mysteries</a>',
    }

    def _get_season(self, local_now):
        """
        returns the current liturgical season using local time
        """
        baptism_of_our_lord = date(local_now.year, 1, 6) + rd(days=1, weekday=SU(+1))
        ash_wednesday = easter(local_now.year) - rd(days=46)
        maundy_thursday = easter(local_now.year) - rd(days=3)
        pentecost = easter(local_now.year) + rd(days=49)
        first_sunday_of_advent = date(local_now.year, 12, 25) - rd(
            days=1, weekday=SU(-4)
        )
        christmas = date(local_now.year, 12, 25)
        season = "ORDINARY"
        if local_now.date() < baptism_of_our_lord:
            season = "CHRISTMAS"
        elif (
            local_now.date() >= baptism_of_our_lord and local_now.date() < ash_wednesday
        ):
            season = "ORDINARY"
        elif local_now.date() >= ash_wednesday and local_now.date() < maundy_thursday:
            season = "LENT"
        elif local_now.date() >= maundy_thursday and local_now.date() < easter(
            local_now.year
        ):
            season = "TRIDUUM"
        elif (
            local_now.date() >= easter(local_now.year) and local_now.date() < pentecost
        ):
            season = "EASTER"
        elif (
            local_now.date() >= pentecost and local_now.date() < first_sunday_of_advent
        ):
            season = "ORDINARY"
        elif (
            local_now.date() >= first_sunday_of_advent and local_now.date() < christmas
        ):
            season = "ADVENT"
        elif local_now.date() >= christmas:
            season = "CHRISTMAS"
        return season

    def _get_upper_day_of_week(self, local_now):
        """
        returns the current day of week spelled out and uppercased
        """
        day_of_week = local_now.date().strftime("%A").upper()
        return day_of_week

    def get_record(self, localtime):
        """
        returns a context json of the current liturgical date
        """
        season_string = self._get_season(localtime)
        dow_string = self._get_upper_day_of_week(localtime)
        rosary_record = {}
        if dow_string == "SUNDAY" and season_string == "ADVENT":
            rosary_record = self.JOYFUL
        elif dow_string == "SUNDAY" and season_string == "LENT":
            rosary_record = self.SORROWFUL
        elif dow_string == "SUNDAY" and season_string == "TRIDUUM":
            rosary_record = self.SORROWFUL
        elif dow_string == "SUNDAY":
            rosary_record = self.GLORIOUS
        elif dow_string == "MONDAY":
            rosary_record = self.JOYFUL
        elif dow_string == "TUESDAY":
            rosary_record = self.SORROWFUL
        elif dow_string == "WEDNESDAY":
            rosary_record = self.GLORIOUS
        elif dow_string == "THURSDAY":
            rosary_record = self.LUMINOUS
        elif dow_string == "FRIDAY":
            rosary_record = self.SORROWFUL
        elif dow_string == "SATURDAY":
            rosary_record = self.JOYFUL
        return rosary_record
