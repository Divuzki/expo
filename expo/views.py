import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.db.models import Q
from .utils import import_docx
from .models import Document, Chapter, Textz, PassCode as Pass

# Home page view


def home_view(request, id=None):
    passcode = request.COOKIES.get('pass_code', False)
    if passcode and not passcode == "":
        qs = Pass.objects.filter(passcode=passcode).first()
        if not qs is None:
            if qs.used_count <= 2:
                if id:
                    qs = Chapter.objects.filter(id=id).first()
                    return render(request, "p/cpage.html", {"chapter": qs})
                else:
                    qs = Chapter.objects.all()
                    return render(request, "p/home.html", {"chapters": qs})
            else:
                res = redirect(
                    "/ex/pchekr/?e=your+code+has+exceeded+its+usage")
                return res
        else:
            return redirect("/ex/pchekr/")
    else:
        return redirect("/ex/pchekr/")

# Displaying search results page view


class Search(TemplateView):
    model = Textz
    template_name = 'p/search.html'

    # Get searched string or None
    def get_query(self, *args, **kwargs):
        if self.request.GET.get('query'):
            return self.request.GET.get('query').split(' ')
        else:
            return None

    # Run the query
    def get_result(self, q, *args, **kwargs):
        return self.model.objects.filter(Q(paragraph__icontains=q)).distinct()

    # Check if query returned anything and merge all result lists
    def get_queryset(self, *agrs, **kwargs):
        results = []
        passcode = self.request.COOKIES.get('pass_code', False)
        if passcode:
            qs = Pass.objects.filter(passcode=passcode).first()
            if not qs is None and qs.used_count <= 2:
                if not self.get_query():
                    return None
                else:
                    for q in self.get_query():
                        if results == []:
                            results = self.get_result(q)
                        else:
                            results = list(
                                set(results) & set(self.get_result(q)))
            else:
                return redirect("/ex/pchekr/")
        else:
            return redirect("/ex/pchekr/")
        return results

    # Send all necessary variables to page render
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query') or ''
        context['results'] = self.get_queryset()
        return context


def passcode_checker(request):
    res = render(request, "p/pcheck.html")
    if request.method == "POST":
        res.set_cookie('pass_code', False, max_age=0)
        res.set_cookie('pass-code-used', False, max_age=0)
        passcode = request.COOKIES.get('pass_code', False)
        code = request.POST.get('pass_code').strip()
        if passcode and not passcode == "":
            code = passcode
        if code == "" or code == None:
            res = render(request, "p/pcheck.html",
                         {"error": "You need to enter your passcode na! 🤦🏾‍♂️"})
        else:
            qs = Pass.objects.filter(passcode=code).first()
            if not qs is None:
                if qs.used_count >= 2:
                    res = render(request, "p/pcheck.html", {
                        "error": "Sorry, You have exceeded your passcode usage 🙆🏾‍♂️ <strong style='color: brown;'>JUST GO AND BUY ANOTHER ONE</strong>"})
                else:
                    qs.used_count = qs.used_count + 1
                    # replace redirect with HttpResponse or render
                    res = redirect("/ex/")
                    res.set_cookie('pass_code', qs.passcode, max_age=7200)
                    res.set_cookie('pass-code-used',
                                   qs.used_count, max_age=7200)
                    qs.save()
            else:
                try_error = request.COOKIES.get('try-error', False)
                if try_error:
                    error = "JUST REST 🥱. Your Code don't exists"
                else:
                    error = "Oga, your code nor dey exists! 🤣, <b>GO AND BUY</b>"
                res = render(request, "p/pcheck.html",
                             {"error": error})
                res.set_cookie('try-error', True, max_age=120*120)
        return res
    else:
        return res

# remove all cookies


def end_session(request):
    res = redirect("/ex/pchekr/")
    res.delete_cookie('pass_code')
    res.delete_cookie('pass-code-used')
    return res


def paymentComplete(request, tId=None):
    if request.method == "POST":
        body = json.loads(request.body)
        n = body['newId']
        if n:
            qs = Pass.objects.create(transactionId=n)
            qs.save()
            data = {
                "msg": "Payment Completed!",
                "code": qs.passcode
            }
            return JsonResponse(data, safe=False)

    elif request.method == "GET":
        lookup = request.GET.get('lookup')

        if lookup:
            lookup = "yes"
        else:
            lookup = "no"

        code = Pass.objects.filter(transactionId=tId).first()

        res = render(request, "p/pshow.html",
                     {"lookingup": True, "error": "TransactionID do not exists!"})
        if not code is None:
            res = render(request, "p/pshow.html",
                         {
                             "code": code.passcode,
                             "tId": code.transactionId,
                             "used_count": code.used_count,
                             "lookup": lookup
                         })
        return res


def passcode_looker(request):
    if request.method == "GET":
        return render(request, "p/pshow.html", {"lookingup": True})
    elif request.method == "POST":
        tId = request.POST.get('transactionId').strip()
        qs = Pass.objects.filter(transactionId=tId).first()
        res = redirect(f"/ex/p/complete/{tId}/?lookup=True")
        if not qs is None:
            if qs.used_count >= 2:
                res = render(request, "p/pshow.html",
                             {"lookingup": True, "error": "This Passcode has exceeded its Limit. <b>Its has EXPIRED!</b>"})
        else:
            res = render(request, "p/pshow.html",
                         {"lookingup": True, "error": "This Passcode do not exists!"})
        return res


def buy_code(request):
    return render(request, "p/buy_code.html")

# Uploading document page view


def Upload(request):
    res = render(request, "p/upload.html")
    if request.user.is_authenticated and request.user.is_staff == True:
        if request.method == "POST":
            name = request.POST.get("name")
            file = request.FILES["file"]
            if name and file:
                file = Document.objects.create(file=file)
                file.save()
                import_docx(Chapter, file, Textz, name)
                res = render(request, "p/upload.html",
                             {"msg": "Upload was sucessful"})
        elif request.method == "GET":
            res = render(request, "p/upload.html")
        else:
            res = redirect("/ex/pchekr/")
    return res


def generate_codes(request):
    res = render(request, "p/codeG.html")
    if request.user.is_authenticated and request.user.is_staff == True:
        if request.method == "POST":
            num = request.POST.get("num")
            if num:
                codes = []
                for num in range(0, int(num)):
                    qs = Pass.objects.create()
                    qs.save()
                    codes.append(qs.passcode)
                res = render(request, "p/codeG.html", {"codes": codes})
        elif request.method == "GET":
            res = render(request, "p/codeG.html")
        else:
            res = redirect("/ex/pchekr/")
    return res
