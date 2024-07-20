from django.urls import path
from .views import home, products, about, form, product_detail, contact, signup, add_to_cart, cart, remove_from_cart, checkout

urlpatterns = [
    path("", home, name="home_page"),
    path("contact/", contact, name="contact"),
    path("products/", products),
    path("about/", about, name="about"),
    path("product/<id>", product_detail, name="detail"),
    path("form/", form, name="form"),
    path("signup/", signup, name="signup"),
    path("add/<id>", add_to_cart, name="add_to_cart"),
    path("cart", cart, name="view_cart"),
    path("remove_item/<id>", remove_from_cart, name="remove_from_cart"),
    path("checkout", checkout, name="checkout"),
]