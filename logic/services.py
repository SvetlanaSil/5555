import json
import os

from store.models import DATABASE
from django.contrib.auth import get_user


def filtering_category(database: dict[str, dict],
                       category_key: [None, str] = None,
                       ordering_key: [None, str] = None,
                       reverse: bool = False):
    if category_key is not None:
        result = [value for value in database.values() if value[
            "category"] == category_key]  # TODO При помощи фильтрации в list comprehension профильтруйте товары по категории (ключ 'category') в продукте database. Или можете использовать
    else:
        result = list(database.values())  # TODO Трансформируйте словарь словарей database в список словарей
        # В итоге должен быть [dict, dict, dict, ...], где dict - словарь продукта из database
    if ordering_key is not None:
        result.sort(key=lambda x: x[ordering_key],
                    reverse=reverse)  # TODO Проведите сортировку result по ordering_key и параметру reverse
    return result


if __name__ == "__main__":
    test = [
        {'name': 'Клубника', 'discount': None, 'price_before': 500.0,
         'price_after': 500.0,
         'description': 'Сладкая и ароматная клубника, полная витаминов, чтобы сделать ваш день ярче.',
         'rating': 5.0, 'review': 200, 'sold_value': 700,
         'weight_in_stock': 400,
         'category': 'Фрукты', 'id': 2, 'url': 'store/images/product-2.jpg',
         'html': 'strawberry'},

        {'name': 'Яблоки', 'discount': None, 'price_before': 130.0,
         'price_after': 130.0,
         'description': 'Сочные и сладкие яблоки - идеальная закуска для здорового перекуса.',
         'rating': 4.7, 'review': 30, 'sold_value': 70, 'weight_in_stock': 200,
         'category': 'Фрукты', 'id': 10, 'url': 'store/images/product-10.jpg',
         'html': 'apple'}
    ]

    print(filtering_category(DATABASE, 'Фрукты', 'price_after', True) == test)  # True


def view_in_cart(request) -> dict:  # Уже реализовано, не нужно здесь ничего писать
    if os.path.exists("cart.json"):  # Если файл существует
        with open("cart.json", encoding="utf-8") as f:
            return json.load(f)
    user = get_user(request).username  # Получаем авторизированного пользователя
    cart = {user: {'products': {}}}
    with open("cart.json", mode="x", encoding="utf-8") as f:  # Создаём файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart


# TODO Проверьте, а существует ли такой товар в корзине, если нет, то перед тем как его добавить - проверьте есть ли такой
# id товара в вашей базе данных DATABASE, чтобы уберечь себя от добавления несуществующего товара.


def add_to_cart(request, id_product: str) -> bool:
    # cart = view_in_cart()
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]
    if id_product not in DATABASE:
        return False
    if id_product not in cart["products"]:
        cart["products"][id_product] = 1
    else:
        cart["products"][id_product] += 1
    with open("cart.json", mode="w", encoding="utf-8") as f:  # Создаём файл и записываем туда пустую корзину
        json.dump(cart_users, f)
    return True


def remove_from_cart(request, id_product: str) -> bool:
    # cart = view_in_cart()
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]
    if id_product not in cart["products"]:
        return False
    cart["products"].pop(id_product)
    with open("cart.json", mode="w", encoding="utf-8") as f:
        json.dump(cart_users, f)
    return True


if __name__ == "__main__":
    # Проверка работоспособности функций view_in_cart, add_to_cart, remove_from_cart
    # Для совпадения выходных значений перед запуском скрипта удаляйте появляющийся файл 'cart.json' в папке
    print(view_in_cart())  # {'products': {}}
    print(add_to_cart('1'))  # True
    print(add_to_cart('0'))  # False
    print(add_to_cart('1'))  # True
    print(add_to_cart('2'))  # True
    print(view_in_cart())  # {'products': {'1': 2, '2': 1}}
    print(remove_from_cart('0'))  # False
    print(remove_from_cart('1'))  # True
    print(view_in_cart())  # {'products': {'2': 1}}


def add_user_to_cart(request, username: str) -> None:
    cart_users = view_in_cart(request)  # Чтение всей базы корзины
    cart = cart_users.get(username)
    if not cart:
        with open("cart.json", mode="w", encoding="utf-8") as f:
            cart_users[username] = {"products": {}}
            json.dump(cart_users, f)


def add_user_to_wishlist(request, username: str) -> None:
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users.get(username)
    if not wishlist:
        with open("wishlist.json", mode="w", encoding="utf-8") as f:
            wishlist_users[username] = {"products": []}
            json.dump(wishlist_users, f)


def view_in_wishlist(request) -> dict:
    if os.path.exists("wishlist.json"):
        with open("wishlist.json", encoding="utf-8") as f:
            return json.load(f)

    user = get_user(request).username
    wishlist = {user: {"products": []}}
    with open("wishlist.json", mode="x", encoding="utf-8") as f:
        json.dump(wishlist, f)

    return wishlist


def add_to_wishlist(request, id_product: str) -> bool:
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]
    if id_product not in DATABASE:
        return False
    if id_product not in wishlist["products"]:
        wishlist["products"].append(id_product)
    with open("wishlist.json", mode="w", encoding="utf-8") as f:
        json.dump(wishlist_users, f)

    return True


def remove_from_wishlist(request, id_product: str) -> bool:
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]
    if id_product not in wishlist["products"]:
        return False
    wishlist["products"].remove(id_product)
    with open("wishlist.json", mode="w", encoding="utf-8") as f:
        json.dump(wishlist_users, f)

    return True
