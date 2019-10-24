from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import Account, Case

# chat
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.http import Http404, HttpResponseForbidden


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
            response = HttpResponse(f'<pre>Case ID: <b>{case_id}</b><br><br>{case}</pre>')
        else:
            response = None  # todo: redirect to own profile
        return response


class About(TemplateView):
    template_name = 'dash_kijiji/about.html'


class HomeView(TemplateView):
    template_name = 'dash_kijiji/home.html'

