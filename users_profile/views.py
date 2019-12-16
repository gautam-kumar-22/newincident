# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View, ListView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from incident.models import Incident, Task

import datetime
import pytz


@method_decorator(lambda x: login_required(x, login_url=reverse_lazy('login')), name='dispatch')
class BaseLoginRequired(View):
    """Check user is login or not."""
    pass


class DashboardView(BaseLoginRequired, View):
    """Dashboard view."""
    template_name = 'welcome.html'

    def get(self, request):
        """Dashboard info."""
        context = {}
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        date_from= pytz.UTC.localize(date_from)
        context['user'] = request.user
        context['all_incident_count'] = Incident.objects.all().count()
        context['latest_incident_count'] = Incident.objects.filter(timestamp__gte=date_from).count()
        context['open_incident_count'] = Incident.objects.filter(status='open').count()
        context['closed_incident_count'] = Incident.objects.filter(status='closed').count()
        context['inprogress_incident_count'] = Incident.objects.filter(status='in_progress').count()
        context['pending_incident_count'] = Incident.objects.filter(status='pending').count()
        context['all_task_count'] = Task.objects.all().count()
        context['my_task_count'] = Task.objects.filter(assigned_user=self.request.user).count()
        return render(request, self.template_name, context=context)


class LoginView(View):
    """Login view."""

    login_template_name = 'login.html'

    def get(self, request):
        """If user will be already login then redirect to welcome page else redirect to login page."""
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, self.login_template_name, {})

    def post(self, request, *args, **kwargs):
        """Login user and redirect them to related template as per the condition."""
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.error(request, 'Incorrect Username or Password ')
        return HttpResponseRedirect(reverse('login'))


class LogoutView(View):
    """Logout to user."""

    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        """Logout to user."""
        logout(request)
        return redirect('login')
