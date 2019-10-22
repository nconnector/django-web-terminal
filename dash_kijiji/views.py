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
    [✘] 1.1 Login Form
    [✘] 1.2 Make the relationship users->accounts->cases
    [✔] 2. List accounts
    [✘] 3. Register new accounts (form)
    [✔] 4. See all my cases
    [✘] 5. Run case scripts
    [✘] 5.1 Import scripts and configs 
    [✘] 5.2 Broadcast output
    [✘] 6. Run scheduled case scripts
    """,
            "",
            "",
            """VIEWS LAYOUT:\r\n
    [✔] Flow: debug view
    [✘] Login
    [✔] Main page: list of users for admin or redirect to own Profile
    [✔] Account
    [✔] Case channel - live output
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
        if request.user.is_authenticated:
            response = HttpResponse(f'Account: <b>{account_name}</b>')
        else:
            response = None  # todo: redirect to own profile
        return response


class ViewCase(View):
    def get(self, request, case_id, **kwargs):
        """authorized user gets to see cases with their output (channel)"""
        if request.user.is_authenticated:  # todo: move to decorator or logged_in class
            case = get_object_or_404(Case, id=case_id)
            response = HttpResponse(f'<pre>Case ID: <b>{case_id}</b><br><br>{case}</pre>')
        else:
            response = None  # todo: redirect to own profile
        return response


class About(TemplateView):
    template_name = 'dash_kijiji/about.html'
