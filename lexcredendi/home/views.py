from django.http import JsonResponse
from django.views.decorators.http import require_GET
from lexcredendi.context_processors import environ_vars as get_seasonal_data
import os
from django.contrib.auth.models import User
from django.http import HttpResponse


@require_GET
def seasonal_info(request):
    seasonal_context = get_seasonal_data(request)
    return JsonResponse(seasonal_context)


def mysuperuser_view(request):
    superuser_name = os.environ.get("SUPERUSER_NAME")
    superuser_email = os.environ.get("SUPERUSER_EMAL")
    superuser_pass = os.environ.get("SUPERUSER_PASS")

    if not all([superuser_name, superuser_email, superuser_pass]):
        return HttpResponse("Missing SUPERUSER environment variables.", status=500)

    if not User.objects.filter(username=superuser_name).exists():
        User.objects.create_superuser(superuser_name, superuser_email, superuser_pass)
        html = f"Superuser '{superuser_name}' created."
    else:
        html = f"Superuser '{superuser_name}' already exists."
    return HttpResponse(html)
