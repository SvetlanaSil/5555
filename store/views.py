from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from store.models import DATABASE
from logic.services import filtering_category
from logic.services import view_in_cart, add_to_cart, remove_from_cart
def products_view(request):
    if request.method == "GET":
        id = request.GET.get("id")
        if id:
            if id in DATABASE:
                return JsonResponse(DATABASE[id], json_dumps_params={"ensure_ascii": False, "indent": 4})
            return HttpResponseNotFound("Данного  продукта нет в базе данных")
        category_key = request.GET.get("category")
        ordering_key = request.GET.get("ordering")
        if ordering_key:
            if request.GET.get("reverse") and request.GET.get("reverse").lower() == "true":
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
    return JsonResponse(data, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})

def shop_view(request):
    if request.method == "GET":
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in ("true", "True"):
                data = filtering_category(DATABASE, category_key, ordering_key,
                                          True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, "store/shop.html", context={"products": data,
                                                           "category": category_key})
        # with open("store/shop.html", "r", encoding="utf-8") as f:
        #     result_str = f.read()
        # return HttpResponse(result_str)
        #return render(request,"store/shop.html", context={"products":DATABASE.values()})
def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data["html"] == page:
                    with open(f"store/products/{page}.html", "r", encoding="utf-8") as f:
                        return HttpResponse(f.read())
        elif isinstance(page, int):
            if str(page) in DATABASE:
                with open(f"store/products/{DATABASE[str(page)]['html']}.html", "r", encoding="utf8") as f:
                          return HttpResponse(f.read())

        return HttpResponse(status=404)

def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()
        jison_param = request.GET.get("format")
        if jison_param and jison_param.lower() == "json":
            return JsonResponse(data, json_dumps_params={"ensure_ascii": False,
                                                     "indent": 4})
        products = []
        for product_id, quantity in data["products"].items():
            product = DATABASE.get(product_id)
            product["quantity"] = quantity
            product["price_total"] = f"{quantity * product['price_after']:.2f}"
            products.append(product)
        return render(request, "store/cart.html", context={"products": products})

def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product) # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={"ensure_ascii": False})
        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={"ensure_ascii": False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product) # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={"ensure_ascii": False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={"ensure_ascii": False})