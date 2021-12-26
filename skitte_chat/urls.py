# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('room', views.index, name='index'),
    path('room/<str:room_name>/', views.room_redirect, name='room'),
    path('room/<str:room_name>/<str:slug>/', views.chat_room, name='chatroom'),
    path('inbox/', views.ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', views.CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', views.ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/',
         views.CreateMessage.as_view(), name='create-message'),
    
    path('', views.chat_index, name='chat_index'),
    # path('save_message/', views.save_message, name='chat_save_message'),
    path('inbox/<int:pk>/create-direct-message/', views.save_dm, name='chat_save_dm'),
]
