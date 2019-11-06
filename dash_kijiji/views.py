from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import get_user_model
from .models import Case


class Login(View):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            response = HttpResponse(f'Login page')
            return response
        else:
            pass  # todo: redirect to main


class Main(View):
    """todo: redirect to own profile if not admin"""
    def get(self, request, **kwargs):
        context = {'account_list': get_user_model().objects.all()}
        return render(request, "dash_kijiji/account_list.html", context)


class ViewCase(View):
    def get(self, request, case_id, **kwargs):
        """authorized user gets to see cases with their output (channel)"""
        if request.user.is_authenticated:  # todo: move to decorator or logged_in class
            case = get_object_or_404(Case, id=case_id)
            context = {'case_log_history': case.log_history(count=20), 'case': case}
            return render(request, "dash_kijiji/case_terminal.html", context)
        else:
            response = None  # todo: redirect to login profile
            return response

    def post(self, request, *args, **kwargs):  # todo: auth this!
        case = get_object_or_404(Case, id=request.POST['case_id'])
        action = request.POST.get('action')
        if action == 'run':
            case.process_open()
        elif action == 'kill':
            case.process_kill()
        elif action == 'status':
            case.process_status()
        return JsonResponse({"post_success": True, "a": action})


class About(TemplateView):
    template_name = 'dash_kijiji/about.html'
