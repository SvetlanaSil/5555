from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from store.models import DATABASE
def products_view(request):
    if request.method == "GET":
        return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False, 'indent': 4})
def shop_view(request):
    if request.method == "GET":
        with open("store/shop.html", "r", encoding="utf-8") as f:
            result_str = f.read()
        return HttpResponse(result_str)

