from datetime import date
from django.utils import timezone
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd
from dateutil.relativedelta import SU


def environ_vars(request):
    baptism_of_our_lord = date(timezone.localtime().year, 1, 6) + rd(
        days=1, weekday=SU(+1)
    )
    ash_wednesday = easter(timezone.localtime().year) - rd(days=46)
    maundy_thursday = easter(timezone.localtime().year) - rd(days=3)
    pentecost = easter(timezone.localtime().year) + rd(days=49)
    first_sunday_of_advent = date(timezone.localtime().year, 12, 25) - rd(
        days=1, weekday=SU(-4)
    )
    christmas = date(timezone.localtime().year, 12, 25)

    data = {}
    current_date = timezone.localtime().date()

    if current_date < baptism_of_our_lord:
        data["SEASONAL_COLOR_CLASS"] = "bg-christmas-gold"
        data["SEASONAL_HIGHLIGHT_CLASS"] = "bg-christmas-gold-light"
        data["SEASON_NAME"] = "Christmas"
    elif baptism_of_our_lord <= current_date < ash_wednesday:
        data["SEASONAL_COLOR_CLASS"] = "bg-ordinary-green"
        data["SEASONAL_HIGHLIGHT_CLASS"] = "bg-ordinary-green-light"
        data["SEASON_NAME"] = "Ordinary Time"
    elif ash_wednesday <= current_date < maundy_thursday:
        data["SEASONAL_COLOR_CLASS"] = "bg-lent-purple"
        data["SEASONAL_HIGHLIGHT_CLASS"] = "bg-lent-purple-light"
        data["SEASON_NAME"] = "Lent"
    elif maundy_thursday <= current_date < easter(timezone.localtime().year):
        data["SEASONAL_COLOR_CLASS"] = "bg-triduum-red"
        data["SEASONAL_HIGHLIGHT_CLASS"] = "bg-triduum-red-light"
        data["SEASON_NAME"] = "Triduum"
    elif easter(timezone.localtime().year) <= current_date < pentecost:
        data["SEASONAL_COLOR_CLASS"] = "bg-easter-gold"
        data["SEASONAL_HIGHLIGHT_CLASS"] = "bg-easter-gold-light"
        data["SEASON_NAME"] = "Easter"
    elif pentecost <= current_date < first_sunday_of_advent:
        data["SEASONAL_COLOR_CLASS"] = "bg-ordinary-green"
        data["SEASONAL_HIGHLIGHT_CLASS"] = "bg-ordinary-green-light"
        data["SEASON_NAME"] = "Ordinary Time"
    elif first_sunday_of_advent <= current_date < christmas:
        data["SEASONAL_COLOR_CLASS"] = "bg-advent-purple"
        data["SEASONAL_HIGHLIGHT_CLASS"] = "bg-advent-purple-light"
        data["SEASON_NAME"] = "Advent"
    elif current_date >= christmas:
        data["SEASONAL_COLOR_CLASS"] = "bg-christmas-gold"
        data["SEASONAL_HIGHLIGHT_CLASS"] = "bg-christmas-gold-light"
        data["SEASON_NAME"] = "Christmas"
    return data
