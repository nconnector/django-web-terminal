from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.http import HttpResponse
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


@method_decorator(login_required, name='dispatch')  # todo: enforce admin account for login_required
class Main(View):
    """todo: redirect to own profile if not admin"""
    def get(self, request, **kwargs):
        context = {'account_list': Account.objects.all()}
        return render(request, "dash_kijiji/account_list.html", context)


class ViewAccount(View):
    def get(self, request, account_name, **kwargs):
        """authorized user gets to see profiles"""
        username = request.user.username if request.user.is_authenticated else None  # todo: move to decorator or logged_in class

        if username:
            response = HttpResponse(f'Account: <b>{account_name}</b>')
        else:
            response = None  # todo: redirect to own profile
        return response


class ViewCase(View):
    def get(self, request, case_id, **kwargs):
        """authorized user gets to see profiles"""
        username = request.user.username if request.user.is_authenticated else None  # todo: move to decorator or logged_in class
        if username:
            case = get_object_or_404(Case, id=case_id)
            response = HttpResponse(f'<pre>Case ID: <b>{case_id}</b><br><br>{case}</pre>')
        else:
            response = None  # todo: redirect to own profile
        return response


class About(TemplateView):
    template_name = 'dash_kijiji/about.html'
