from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.http import HttpResponse

# Create your views here.


class Flow(View):
    def get(self, request, *args, **kwargs):
        workflow = [
            """FEATURES LAYOUT:\r\n
    [✔] 0. MongoDB integration
    [✔] 1. Login cabability
    [✘] 1.1. Login Form
    [✘] 1.2. Make Cases from Users, not Clients
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
    [✘] Welcome: if logged_in
    [✘] My Profile
    [✘] About
    """,

        ]
        response = HttpResponse(f'<pre>HTTPRESPONSE\n\n{"<br>".join(workflow)}</pre>')
        return response


class Login(View):
    def get(self, request, **kwargs):
        response = HttpResponse(f'Login page')
        return response


class Main(View):
    def get(self, request, **kwargs):
        response = HttpResponse(f'Main page')
        return response


class Profile(View):
    def get(self, request, **kwargs):
        response = HttpResponse(f'My Profile page')
        return response


class About(View):
    def get(self, request, **kwargs):
        response = HttpResponse(f'About page')
        return response

