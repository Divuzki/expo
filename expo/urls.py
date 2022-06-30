from django.urls import path

from .views import (
    home_view,
    Upload,
    Search,
    passcode_checker,
    end_session,
    paymentComplete,
    passcode_looker,
    buy_code,
    generate_codes
)

urlpatterns = [
    path('', home_view, name='home_docx'),
    path('up/', Upload, name='upload_docx'),
    path('search', Search.as_view(), name='search_docx'),
    path('pchekr/', passcode_checker, name="passcode_checker"),
    path('end/', end_session, name="end_session"),
    path('look/', passcode_looker, name="passcode_looker"),
    path('buy/', buy_code, name="buy_passcode"),
    path("p/complete/", paymentComplete, name="payment-completed"),
    path("p/complete/<str:tId>/", paymentComplete, name="show-pass"),
    path('c/<int:id>/', home_view, name='cpage'),
    path('g/', generate_codes, name='gpage'),
]
