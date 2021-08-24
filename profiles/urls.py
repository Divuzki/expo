from django.urls import path, re_path
from .views import (
    profile_detail_view, 
    profile_update_view, 
    friends_view,
    )

urlpatterns = [
    path(r'<str:username>', profile_detail_view, name="profile"),
    re_path(r'u/edit?/', profile_update_view, name="edit-profile"),
    path('<str:username>/friends', friends_view, name="profile-firends"),
]
