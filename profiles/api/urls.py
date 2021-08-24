from django.urls import path

from .views import (
    profile_detail_api_view,
    ProfileDetailUpdateDestroyAPIView,
    UserUpdateAPIView

)
'''
CLIENT
Base ENDPOINT /api/skits/
'''
urlpatterns = [
    path('<str:username>/', profile_detail_api_view),

    path('<str:user__username>/edit/',
         ProfileDetailUpdateDestroyAPIView.as_view()),

    path('edit/<str:username>/',
         UserUpdateAPIView.as_view()),    

    path('<str:username>/follow', profile_detail_api_view),
    path('<str:username>/friend-request/', profile_detail_api_view),
]
