from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('room/<pk>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<pk>', views.update_room, name='update-room'),
    path('delete-room/<pk>', views.delete_room, name='delete-room'),
]
