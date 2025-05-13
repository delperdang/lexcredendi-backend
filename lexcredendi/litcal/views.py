from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET
import logging

from .calendar import (
    Calendar as LitcalCalendar,
)
from .intentions import Intentions
from .mysteries import Mysteries

logger = logging.getLogger(__name__)


@require_GET
def get_liturgical_day_info(request):
    """
    API endpoint to fetch current liturgical calendar information,
    Rosary mysteries, and Papal intentions.
    """
    current_local_time = timezone.localtime(timezone.now())

    data = {
        "current_date_iso": current_local_time.isoformat(),
        "liturgical_calendar": None,
        "rosary_mysteries": None,
        "papal_intentions": None,
        "errors": [],
    }

    try:
        usccb_calendar = LitcalCalendar()
        calendar_record = usccb_calendar.get_record(current_local_time)
        if calendar_record and calendar_record.get("title"):
            data["liturgical_calendar"] = calendar_record
        elif calendar_record:
            data["liturgical_calendar"] = {
                "title": "Calendar Data",
                "text": "Could not parse calendar data fully.",
            }
            logger.warning(
                "Liturgical Calendar utility returned partial/unexpected data."
            )
        else:
            data["errors"].append("Could not retrieve liturgical calendar information.")
            logger.error("Failed to retrieve liturgical calendar information.")
    except Exception as e:
        logger.error(f"Error fetching liturgical calendar: {e}", exc_info=True)
        data["errors"].append(f"Error fetching liturgical calendar: {str(e)}")

    try:
        mysteries_util = Mysteries()
        mysteries_record = mysteries_util.get_record(current_local_time)
        if mysteries_record and mysteries_record.get("title"):
            data["rosary_mysteries"] = mysteries_record
        elif mysteries_record:
            data["rosary_mysteries"] = {
                "title": "Rosary Mysteries",
                "text": "Could not parse mysteries data fully.",
            }
            logger.warning("Rosary Mysteries utility returned partial/unexpected data.")
        else:
            data["errors"].append("Could not determine Rosary mysteries.")
            logger.error("Failed to determine Rosary mysteries.")
    except Exception as e:
        logger.error(f"Error determining Rosary mysteries: {e}", exc_info=True)
        data["errors"].append(f"Error determining Rosary mysteries: {str(e)}")

    try:
        usccb_intentions = Intentions()
        intentions_record = usccb_intentions.get_record(current_local_time)
        if intentions_record and intentions_record.get("title"):
            data["papal_intentions"] = intentions_record
        elif intentions_record:
            data["papal_intentions"] = {
                "title": "Papal Intentions",
                "text": "Could not parse intentions data fully.",
            }
            logger.warning("Papal Intentions utility returned partial/unexpected data.")
        else:
            data["errors"].append("Could not retrieve Papal intentions.")
            logger.error("Failed to retrieve Papal intentions.")
    except Exception as e:
        logger.error(f"Error fetching Papal intentions: {e}", exc_info=True)
        data["errors"].append(f"Error fetching Papal intentions: {str(e)}")

    from lexcredendi.context_processors import environ_vars as get_seasonal_colors_info

    seasonal_info = get_seasonal_colors_info(request)  # Call it directly
    data["seasonal_info"] = {
        "color_class": seasonal_info.get("SEASONAL_COLOR_CLASS"),
        "highlight_class": seasonal_info.get("SEASONAL_HIGHLIGHT_CLASS"),
        "season_name": seasonal_info.get("SEASON_NAME"),
    }

    return JsonResponse(data)
