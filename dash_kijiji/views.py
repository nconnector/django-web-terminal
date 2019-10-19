from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def test(request):
    return HttpResponse(f'HTTPRESPONSE to <br><br>{request.user}<br><br>{["<br>" + i for i in request.__dict__]}')


def flow(request):

    workflow = [
        "[x] 1. Login",
        "[x] 2. Read a new ad",
        "[x] 3. Write a similar ad",
        "[x] 4. See all my ads",
        "[x] 5. Reload ads from scratch",
    ]

    return HttpResponse(f'HTTPRESPONSE<br><br>{"<br>".join(workflow)}')
