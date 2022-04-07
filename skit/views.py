import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.template.loader import get_template
from django import template
from django.core.mail import EmailMessage
from django.core.mail import send_mail as sm
from django.contrib.auth.decorators import login_required
from .models import Skit


ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html")


@login_required
def feed_view(request, *args, **kwargs):
    return render(request, "pages/feed.html")


def skits_list_view(request, *args, **kwargs):
    return render(request, "skits/list.html")


@login_required
def notify_view(request, *args, **kwargs):
    return HttpResponse("Sorry, this feature is not avaliable :(")


def skits_detail_view(request, skit_url, *args, **kwargs):
    qs = Skit.objects.filter(slug=skit_url).first()
    title = ""
    if qs.content:
        title = qs.content
    if qs.caption:
        title = qs.caption
    context = {
        "skit_url": skit_url,
        "title": title,
        "image": qs.image,
        "type": "article"
    }
    return render(request, "skits/detail.html", context)


def skitte_serviceworker(request, js):
    template = get_template('sw.js')
    html = template.render()
    return HttpResponse(html, content_type="application/x-javascript")


def skitte_offline(request, js):
    return render(request, "offline.html")


def mailtest(request, *args, **kwargs):
    res = sm(
        subject='Subject here',
        message='Here is the message.',
        from_email='noreply.skitte@gmail.com',
        recipient_list=['divuzki@gmail.com'],
        fail_silently=False,
    )

    return HttpResponse(f"Email sent to {res} members")
    # return HttpResponse("Email sent to "+ res +" members")


def base_layout(request):
    template = 'base.html'
    return render(request, template)

# custom method for generating predictions
def getPredictions(pclass, sex, age, intrest, parch, fare, C, Q, S):
    import pickle
    model = pickle.load(open("post_ml_model.sav", "rb"))
    sc = pickle.load(open("scaler.sav", "rb"))
    prediction = model.predict(sc.transform([[pclass, sex, age, intrest, parch, fare, C, Q, S]]))
    
    if prediction == 0:
        return "not survived"
    elif prediction == 1:
        return "survived"
    else:
        return "error"
        

# our result page view
def result(request):
    pclass = int(request.GET['pclass'])
    sex = int(request.GET['sex'])
    age = int(request.GET['age'])
    sibsp = int(request.GET['sibsp'])
    parch = int(request.GET['parch'])
    fare = int(request.GET['fare'])
    embC = int(request.GET['embC'])
    embQ = int(request.GET['embQ'])
    embS = int(request.GET['embS'])

    result = getPredictions(pclass, sex, age, sibsp, parch, fare, embC, embQ, embS)

    return render(request, 'result.html', {'result':result})