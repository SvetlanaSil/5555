from django.urls import path
from .views import products_view, shop_view, products_page_view, cart_view, cart_add_view, cart_del_view, \
    cart_remove_view, cart_buy_now_view, delivery_estimate_view, coupon_check_view

app_name = "store"

urlpatterns = [
    path("product/", products_view),
    path("", shop_view, name="shop_view"),
    path("product/<slug:page>.html", products_page_view, name="products_page_view"),
    path("product/<int:page>", products_page_view),
    path("cart/", cart_view, name="cart_view"),
    path("cart/add/<slug:id_product>", cart_add_view),
    path("cart/del/<slug:id_product>", cart_del_view),
    path("coupon/check/<slug:name_coupon>", coupon_check_view),
    path("delivery/estimate", delivery_estimate_view),
    path("cart/buy/<slug:id_product>", cart_buy_now_view, name="buy_now"),
    path("cart/remove/<slug:id_product>", cart_remove_view, name="remove_now")
]