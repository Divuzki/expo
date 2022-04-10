from django.urls import path

from .views import (
    home_view,
    # Upload,
    Search,
    passcode_checker,
    end_session,
    paymentComplete,
    passcode_looker,
    buy_code
)

urlpatterns = [
    path('', home_view, name='home-docx'),
    # path('upload/', Upload.as_view(), name='upload-docx'),
    path('search', Search.as_view(), name='search-docx'),
    path('pchekr/', passcode_checker, name="passcode_checker"),
    path('end/', end_session, name="end_session"),
    path('look/', passcode_looker, name="passcode_looker"),
    path('buy/', buy_code, name="passcode_looker"),
    path("p/complete/", paymentComplete, name="payment-completed"),
    path("p/complete/<str:tId>/", paymentComplete, name="show-pass")
]
