from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

api_v1_urlpatterns = [
    path("home/", include("home.urls")),
    path("apologetics/", include("apologetics.urls")),
    path("art/", include("art.urls")),
    path("bible/", include("bible.urls")),
    path("catechism/", include("catechism.urls")),
    path("doctrine/", include("doctrine.urls")),
    path("litcal/", include("litcal.urls")),
    path("prayer/", include("prayer.urls")),
    path("readings/", include("readings.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tz_detect/", include("tz_detect.urls")),
    path("api/v1/", include(api_v1_urlpatterns)),
    path("", include("home.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
