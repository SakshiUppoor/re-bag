from django.urls import path
from .views import *

urlpatterns = [
    # path('', createProduct, name="create_product"),
    path('room/<slug:slug>', room, name="room"),
    #path('home/', home, name="home"),
    path('signup/', register, name="register"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('shop/', shop, name="shop"),
    path('cart/', cart, name="cart"),
    path('', home, name="home"),
    path('add/',createProduct, name="addProduct"),
    path('product/<slug:slug>',detail, name="detail"),
    path('profile/<int:id>',profile, name="profile"),
    # path('add/',addProduct, name="addProduct"),
    path('myproducts/',addProduct, name="myProducts"),
]
