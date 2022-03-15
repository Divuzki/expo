from django.urls import path

from .views import (
    Home,
    Upload,
    Search
)

urlpatterns = [
    path('', Home.as_view(), name='home-docx'),
    # path('upload/', Upload.as_view(), name='upload-docx'),
    path('search', Search.as_view(), name='search-docx'),
]
