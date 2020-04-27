from django.urls import path
from .views import (
    createProduct,
    room,
    home,
    register,
    user_login,
    user_logout,
    shop,
    categoryShop
)

urlpatterns = [
    path('', createProduct, name="create_product"),
    path('room/<str:room_name>', room, name="room"),
    path('home/', home, name="home"),
    path('signup/', register, name="register"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('shop/', shop, name="shop"),
    path('shop/<str:url_category>', categoryShop, name="categoryShop"),
]
