from django.urls import path
from .views import createProduct, room, home

urlpatterns = [
    path('', createProduct, name="create_product"),
    path('room/<str:room_name>', room, name="room"),
    path('home/', home, name="home"),
]
