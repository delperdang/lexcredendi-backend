from django.http import JsonResponse
from django.views.decorators.http import require_GET
from lexcredendi.context_processors import environ_vars as get_seasonal_data


@require_GET
def seasonal_info(request):
    seasonal_context = get_seasonal_data(request)
    return JsonResponse(seasonal_context)
