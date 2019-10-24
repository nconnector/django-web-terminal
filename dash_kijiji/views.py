from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import Account, Case

from .backend_scripts.stdout_intercept import execute_and_stream


class Login(View):
    def get(self, request, **kwargs):
        response = HttpResponse(f'Login page')
        return response


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
            context = {'case_id': case.id, 'case_log_history': case.log_history(count=20)}
            return render(request, "dash_kijiji/home.html", context)
        else:
            response = None  # todo: redirect to own profile
            return response


class About(TemplateView):
    template_name = 'dash_kijiji/about.html'


class HomeView(View):
    def get(self, request, **kwargs):
        return render(request, "dash_kijiji/home.html")


class Popen(View):
    def get(self, request, script_name, **kwargs):  # todo: case config
        execute_and_stream(['python', '-u', f'dash_kijiji\\backend_scripts\\{script_name}.py'])
        return HttpResponse('')
