from random import random

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

from app_datetime.views import datetime_view
from app_weather.views import current_weather_view
from store.views import products_view, shop_view


def random_view(request):
    if request.method == "GET":
        return HttpResponse(round(random.uniform(1, 100), 4))


urlpatterns = [
    path("", shop_view),
    path("admin/", admin.site.urls),
    path("random/", random_view),
    path("datetime/", datetime_view),
    path("weather/", current_weather_view),
    path("product/", products_view)
]
