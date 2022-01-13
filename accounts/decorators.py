import datetime
from functools import wraps
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test


def confirm_password(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        last_login = request.user.last_login
        timespan = last_login + datetime.timedelta(seconds=6)
        if timezone.now() > timespan:
            from .views import ConfirmPasswordView
            return ConfirmPasswordView.as_view()(request, *args, **kwargs)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def check_user(user):
    return not user.is_authenticated


user_logout_required = user_passes_test(check_user, '/', None)


def auth_user_should_not_access(viewfunc):
    return user_logout_required(viewfunc)