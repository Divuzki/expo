from django.urls import path

from .views import (
    skit_action_view,

    SkitAPIView,
    SkitListView,
    SkitDetailUpdateDestroyAPIView,
)
'''
CLIENT
Base ENDPOINT /api/skits/
'''
urlpatterns = [
    path('', SkitListView.as_view()),
    path('feed/', SkitAPIView.as_view()),
    path('action/', skit_action_view),
    path('create/', SkitAPIView.as_view()),
    path('<slug>/', SkitDetailUpdateDestroyAPIView.as_view()),
    path('<slug>/delete/', SkitDetailUpdateDestroyAPIView.as_view()),
    path('<slug>/edit/', SkitDetailUpdateDestroyAPIView.as_view()),
]
