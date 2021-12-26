from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.views.generic.edit import UpdateView
from .tokens import account_activation_token
from .forms import SignupForm, UserCreationForm, ConfirmPasswordForm

from django.contrib.auth import get_user_model

User = get_user_model()


# Confirming Password
class ConfirmPasswordView(UpdateView):
    form_class = ConfirmPasswordForm
    template_name = 'accounts/confirm_password.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.get_full_path()  # Getting the full url


def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    nxt = request.GET.get('next')
    if form.is_valid():
        user_ = form.get_user()
        login(request, user_)
        if nxt:
            return redirect(f'/{nxt}')
        else:
            return redirect("home")
    context = {
        "form": form,
        "btn_label": "Login",
        "nxt": nxt,
        "title": "Login To Your Skitte Account"
    }
    return render(request, "accounts/auth.html", context)


def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect("/login")
    context = {
        "form": None,
        "discription": "Are you sure you want to logout?",
        "btn_label": "Click to Confirm",
        "title": "Logout"
    }
    return render(request, "accounts/auth.html", context)


def register_view(request, *args, **kwargs):
    form = UserCreationForm()  # Django User Creation Form
    nxt = request.GET.get('next')

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(
                request, username=username, password=password)

            if user is not None:
                login(request, user)
                if nxt:
                    return redirect(f'/{nxt}')
                else:
                    return redirect("/feed")
    context = {
        "form": form,
        "btn_label": "SignUp",
        "nxt": nxt,
        "title": "Create A New Skitte Account"
    }
    return render(request, "accounts/auth.html", context)


def register_views(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            nxt = request.GET.get('next')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate Your New Skitte Account.'
            message = render_to_string('accounts/email_template.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'nxt': nxt
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMultiAlternatives(
                    mail_subject, message, to=[to_email]
            )
            email.attach_alternative(message, "text/html")
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    context = {
        "form": form,
        "btn_label": "SignUp",
        "title": "Create A New Skitte Account"
    }
    return render(request, 'accounts/auth.html', context)


def activate(request, uidb64, token):
    nxt = request.GET.get('next')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        if user is not None:
            if nxt:
                return redirect(f'/{nxt}')
            else:
                return redirect("/feed")
    else:
        return HttpResponse('Activation link is invalid!')






# Notification
# class PostNotification(View):
#     def get(self, request, notification_pk, post_pk, *args, **kwargs):
#         notification = Notification.objects.get(pk=notification_pk)
#         post = Skit.objects.get(pk=post_pk)

#         notification.user_has_seen = True
#         notification.save()

#         return redirect('post-detail', pk=post_pk)


# class FollowNotification(View):
#     def get(self, request, notification_pk, profile_pk, *args, **kwargs):
#         notification = Notification.objects.get(pk=notification_pk)
#         profile = UserProfile.objects.get(pk=profile_pk)

#         notification.user_has_seen = True
#         notification.save()

#         return redirect('profile', pk=profile_pk)


# class ThreadNotification(View):
#     def get(self, request, notification_pk, object_pk, *args, **kwargs):
#         notification = Notification.objects.get(pk=notification_pk)
#         thread = PrivateThreadModel.objects.get(pk=object_pk)

#         notification.user_has_seen = True
#         notification.save()

#         return redirect('thread', pk=object_pk)


# class RemoveNotification(View):
#     def delete(self, request, notification_pk, *args, **kwargs):
#         notification = Notification.objects.get(pk=notification_pk)

#         notification.user_has_seen = True
#         notification.save()

#         return HttpResponse('Success', content_type='text/plain')
