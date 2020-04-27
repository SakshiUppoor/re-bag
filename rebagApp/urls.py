from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # path('', createProduct, name="create_product"),
    path('room/<str:room_name>', room, name="room"),
    # path('home/', home, name="home"),
    path('shop/', views.shop, name="shop"),
    path('shop/<str:url_category>', views.categoryShop, name="categoryShop"),
    path('',views.addProduct, name="addProduct")
]
