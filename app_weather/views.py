from django.shortcuts import render
from django.http import JsonResponse
from weather_api import current_weather


def current_weather_view(request):
    if request.method == "GET":
       # data = current_weather(55.75, 37.61)
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")
        if lat and lon:
            data = current_weather(lat=lat, lon=lon)
        else:
            data = current_weather(55.75, 37.61)
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})
