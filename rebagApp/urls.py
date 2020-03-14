from django.urls import path
from .views import createProduct, room

urlpatterns = [
    path('', createProduct, name="create_product"),
    path('room/<str:room_name>', room, name="room"),
]
