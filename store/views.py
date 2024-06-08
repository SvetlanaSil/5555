from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from store.models import DATABASE
from logic.services import filtering_category
from logic.services import view_in_cart, add_to_cart, remove_from_cart
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required


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
        # return render(request,"store/shop.html", context={"products":DATABASE.values()})


# def products_page_view(request, page):
#     if request.method == "GET":
#         if isinstance(page, str):
#             for data in DATABASE.values():
#                 if data["html"] == page:
#                     with open(f"store/products/{page}.html", "r", encoding="utf-8") as f:
#                         return HttpResponse(f.read())
#         elif isinstance(page, int):
#             if str(page) in DATABASE:
#                 with open(f"store/products/{DATABASE[str(page)]['html']}.html", "r", encoding="utf8") as f:
#                           return HttpResponse(f.read())
#
#         return HttpResponse(status=404)


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data["html"] == page:
                    return render(request, "store/product.html", context={"product": data})

        elif isinstance(page, int):
            # Обрабатываем условие того, что пытаемся получить страницу товара по его id
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:
                return render(request, "store/product.html", context={"product": data})

        return HttpResponse(status=404)


# def cart_view(request):
#    if request.method == "GET":
#        data = view_in_cart()
#        jison_param = request.GET.get("format")
#         if jison_param and jison_param.lower() == "json":
#            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
#                                                         'indent': 4})
#        return render(request, "store/cart.html")
@login_required(login_url="login:login_view")
def cart_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_cart(request)[current_user]
        if request.GET.get("format") == "JSON":
            return JsonResponse(data, json_dumps_params={"ensure_ascii": False,
                                                         "indent": 4})
        products = []
        for product_id, quantity in data["products"].items():
            product = DATABASE.get(product_id)
            product["quantity"] = quantity
            product["price_total"] = f"{quantity * product['price_after']:.2f}"
            products.append(product)

        return render(request, "store/cart.html", context={"products": products})


@login_required(login_url="login:login_view")
def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={"ensure_ascii": False})
        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={"ensure_ascii": False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product)  # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={"ensure_ascii": False})
        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={"ensure_ascii": False})


def coupon_check_view(request, name_coupon):
    # DATA_COUPON - база данных купонов: ключ - код купона (name_coupon); значение - словарь со значением скидки в процентах и
    # значением действителен ли купон или нет
    DATA_COUPON = {
        "coupon": {
            "value": 10,
            "is_valid": True},
        "coupon_old": {
            "value": 20,
            "is_valid": False},
    }
    if request.method == "GET":
        if name_coupon in DATA_COUPON:
            coupon = DATA_COUPON[name_coupon]
            return JsonResponse({
                'is_valid': coupon['is_valid'],
                'discount': coupon['value']
            })
        return HttpResponseNotFound('Неверный купон')

        # TODO Проверьте, что купон есть в DATA_COUPON, если он есть, то верните JsonResponse в котором по ключу "discount"
        # получают значение скидки в процентах, а по ключу "is_valid" понимают действителен ли купон или нет (True, False)

        # TODO Если купона нет в базе, то верните HttpResponseNotFound("Неверный купон")


def delivery_estimate_view(request):
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 80},
            "Санкт-Петербург": {"price": 50},
            "fix_price": 100,
        },
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        if country in DATA_PRICE:
            if city in DATA_PRICE[country]:
                return JsonResponse({'price': DATA_PRICE[country][city]['price']})
            else:
                return JsonResponse({'price': DATA_PRICE[country]['fix_price']})
        return HttpResponseNotFound('Неверные данные')
        # TODO Реализуйте логику расчёта стоимости доставки, которая выполняет следующее:
        # Если в базе DATA_PRICE есть и страна (country) и существует город(city), то вернуть JsonResponse со словарём, {"price": значение стоимости доставки}
        # Если в базе DATA_PRICE есть страна, но нет города, то вернуть JsonResponse со словарём, {"price": значение фиксированной стоимости доставки}
        # Если нет страны, то вернуть HttpResponseNotFound("Неверные данные")


@login_required(login_url="login:login_view")
def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)
        if result:
            return redirect("store:cart_view")
        return HttpResponseNotFound("Неудачное добавление в корзину")


def cart_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product)  # TODO Вызвать функцию удаления из корзины
        if result:
            return redirect("store:cart_view")  # TODO Вернуть перенаправление на корзину

        return HttpResponseNotFound("Неудачное удаление из корзины")
