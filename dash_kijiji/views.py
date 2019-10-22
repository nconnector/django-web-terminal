from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Account, Case


# Create your views here.
class Flow(View):
    def get(self, request, *args, **kwargs):
        workflow = [
            """FEATURES LAYOUT:\r\n
    [✔] 0. MongoDB integration
    [✔] 1. Login cabability
    [✘] 1.1. Login Form
    [✘] 1.2. Make Cases from Users, not Accounts
    [✔] 2. Read a new ad
    [✘] 2. Parse the newly read ad ❤
    [✘] 3. Write a similar ad
    [✘] 4. See all my ads
    [✘] 5. Reload ads from scratch
    """,
            "",
            "",
            """VIEWS LAYOUT:\r\n
    [✔] Flow: debug view
    [✘] Login
    [✘] Main page: list of users for admin or redirect to own Profile
    [✘] Profile
    [✔] About
    [✘] Extendable Base Page for {% extends %}
    """,

        ]
        response = HttpResponse(f'<pre>HTTPRESPONSE\n\n{"<br>".join(workflow)}</pre>')
        return response


class Login(View):
    def get(self, request, **kwargs):
        response = HttpResponse(f'Login page')
        return response


@method_decorator(login_required, name='dispatch')
class Main(View):
    """
    todo: redirect to own profile if not admin
    """
    def get(self, request, **kwargs):
        context = {'account_list': Account.objects.all()}
        return render(request, "dash_kijiji/account_list.html", context)


class Profile(View):
    def get(self, request, username, **kwargs):
        admin = True
        if admin:
            response = HttpResponse(f'Profile page for <b>{username}</b>')
        else:
            response = None  # todo: redirect to own profile
        return response


class About(TemplateView):
    template_name = 'dash_kijiji/about.html'
