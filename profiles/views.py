from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import ProfileForm
from .models import Profile, FriendRequest
from django.http import JsonResponse
from accounts.decorators import confirm_password
from django.utils.decorators import method_decorator


User = get_user_model()


# @method_decorator(confirm_password, name='dispatch')
@confirm_password
def profile_update_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/login?next=/profile/update")
    user = request.user
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "username": user.username,
    }
    my_profile = user.profile
    form = ProfileForm(request.POST or None,
                       instance=my_profile, initial=user_data)
    if form.is_valid():
        profile_obj = form.save(commit=False)
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()
        profile_obj.save()
    context = {
        "form": form,
        "btn_label": "Save",
        "title": "Update Profile",
    }
    return render(request, "profiles/form.html", context)


def profile_detail_view(request, username, *args, **kwargs):
    # Get the profile for past username
    qs = Profile.objects.filter(user__username=username)
    p = qs.first()
    if not qs.exists():
        raise Http404
    profile_obj = qs.first()
    is_following = False
    if request.user.is_authenticated:
        user = request.user
        is_following = user in profile_obj.followers.all()
    context = {
        "username": username,
        "profile": profile_obj,
        "is_following": is_following,
    }
    return render(request, "profiles/detail.html", context)

@method_decorator(confirm_password, name='dispatch')
def friends_view(request, username, *args, **kwargs):
    context = {
        "username": username,
    }
    return render(request, "profiles/friends.html", context)
