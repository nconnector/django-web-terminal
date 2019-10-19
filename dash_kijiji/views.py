from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):

    flow = [
        "1. Login",
        "2. Read a new ad",
        "3. Write a similar ad",
        "4. See all my ads",
        "5. Reload ads from scratch",
    ]

    return HttpResponse("HTTPRESPONSE")
