from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET
import logging

from .readings import Readings as ReadingsScraper

logger = logging.getLogger(__name__)


@require_GET
def get_daily_readings(request):
    """
    API endpoint to fetch the current day's Mass readings.
    """
    current_local_time = timezone.localtime(timezone.now())

    response_data = {
        "date": current_local_time.strftime("%Y-%m-%d"),
        "readings": [],
        "errors": [],
    }

    try:
        readings_util = ReadingsScraper()
        records = readings_util.get_records(current_local_time)

        if records and not (len(records) == 1 and records[0].get("title") == "Error"):
            response_data["readings"] = records
        elif not records:
            response_data["errors"].append("No readings data returned from scraper.")
            logger.warning("Readings scraper returned no data.")
        else:
            response_data["errors"].append(
                records[0].get("text", "Unknown error from readings scraper.")
            )
            logger.error(
                f"Readings scraper returned an error: {records[0].get('text')}"
            )

    except Exception as e:
        logger.error(f"Error in get_daily_readings view: {e}", exc_info=True)
        response_data["errors"].append(
            f"An unexpected error occurred while fetching readings: {str(e)}"
        )

    return JsonResponse(response_data)
