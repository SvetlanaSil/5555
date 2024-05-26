from django.urls import path
from app_weather.views import current_weather_view

urlpatterns = [
    path("weather/", current_weather_view),
]