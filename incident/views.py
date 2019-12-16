"""Create your views here."""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View, ListView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.db import transaction
from django.utils.safestring import mark_safe

from .models import *
from .utils import Calendar
from .forms import IncidentForm, TaskForm, TaskFormSet, BlogForm
# , RelatedipForm, RelateddomainForm
from users_profile.views import BaseLoginRequired

import calendar
import datetime
import pytz
import xlwt


class CreateIncidentView(BaseLoginRequired, CreateView):
    """Create incident view."""

    model = Incident
    template_name = 'create_incident.html'
    form_class = IncidentForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(CreateIncidentView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['titles'] = TaskFormSet(self.request.POST, self.request.FILES)
            # data['relatedip'] = RelatedipForm(self.request.POST)
            # data['domain'] = RelateddomainForm(self.request.POST)
        else:
            data['titles'] = TaskFormSet()
            # data['relatedip'] = RelatedipForm()
            # data['domain'] = RelateddomainForm()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        # relatedip = context['relatedip']
        # domain = context['domain']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
            # if relatedip.is_valid():
            #     relatedip.instance = self.object
            #     relatedip.save()
            # if titles.is_valid():
            #     domain.instance = self.object
            #     domain.save()
        return super(CreateIncidentView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list-incident')


class UpdateIncidentView(BaseLoginRequired, UpdateView):
    """Update incident view."""

    model = Incident
    template_name = 'create_incident.html'
    form_class = IncidentForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(UpdateIncidentView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['titles'] = TaskFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['titles'] = TaskFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(UpdateIncidentView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list-incident')


class ListIncidentView(BaseLoginRequired, ListView):
    model = Incident
    template_name = "incident_list.html"
    context_object_name = 'incidents_list'
    # paginate_by = 20

    def get_context_data(self, **kwargs):
        """Add section data in context."""
        context = super(ListIncidentView, self).get_context_data(**kwargs)
        context['all_incident'] = 'all_incident'
        return context


class IncidentDetailView(BaseLoginRequired, DetailView):

    model = Incident
    template_name = 'incident_detail.html'

    def get_context_data(self, **kwargs):
        context = super(IncidentDetailView, self).get_context_data(**kwargs)
        context['all_comment'] = Comment.objects.filter(incident=context['incident']).order_by('created_on')
        return context


class OpenIncidentView(BaseLoginRequired, ListView):
    model = Incident
    template_name = "incident_list.html"
    context_object_name = 'incidents_list'
    # paginate_by = 20

    def get_queryset(self):
        incidents_list = Incident.objects.filter(status='open')
        return incidents_list

    def get_context_data(self, **kwargs):
        """Add section data in context."""
        context = super(OpenIncidentView, self).get_context_data(**kwargs)
        context['open_incident'] = 'open_incident'
        return context


class ClosedIncidentView(BaseLoginRequired, ListView):
    model = Incident
    template_name = "incident_list.html"
    context_object_name = 'incidents_list'
    # paginate_by = 20

    def get_queryset(self):
        incidents_list = Incident.objects.filter(status='closed')
        return incidents_list

    def get_context_data(self, **kwargs):
        """Add section data in context."""
        context = super(ClosedIncidentView, self).get_context_data(**kwargs)
        context['close_incident'] = 'close_incident'
        return context


class InprogressIncidentView(BaseLoginRequired, ListView):
    model = Incident
    template_name = "incident_list.html"
    context_object_name = 'incidents_list'
    # paginate_by = 20

    def get_queryset(self):
        incidents_list = Incident.objects.filter(status='in_progress')
        return incidents_list

    def get_context_data(self, **kwargs):
        """Add section data in context."""
        context = super(InprogressIncidentView, self).get_context_data(**kwargs)
        context['inprogress_incident'] = 'inprogress_incident'
        return context

class PendingIncidentView(BaseLoginRequired, ListView):
    model = Incident
    template_name = "incident_list.html"
    context_object_name = 'incidents_list'
    # paginate_by = 20

    def get_queryset(self):
        incidents_list = Incident.objects.filter(status='pending')
        return incidents_list

    def get_context_data(self, **kwargs):
        """Add section data in context."""
        context = super(PendingIncidentView, self).get_context_data(**kwargs)
        context['pending_incident'] = 'pending_incident'
        return context


class LatestIncidentView(BaseLoginRequired, ListView):
    model = Incident
    template_name = "incident_list.html"
    context_object_name = 'incidents_list'
    paginate_by = 20

    def get_queryset(self):
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        date_from= pytz.UTC.localize(date_from)
        incidents_list = Incident.objects.filter(timestamp__gte=date_from)
        return incidents_list

    def get_context_data(self, **kwargs):
        """Add section data in context."""
        context = super(LatestIncidentView, self).get_context_data(**kwargs)
        context['latest_incident'] = 'latest_incident'
        return context


class MyIncidentView(BaseLoginRequired, ListView):
    model = Incident
    template_name = "incident_list.html"
    context_object_name = 'incidents_list'
    paginate_by = 20

    def get_queryset(self):
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        date_from= pytz.UTC.localize(date_from)
        incidents_list = Incident.objects.filter(assigned_user=self.request.user)
        return incidents_list

    def get_context_data(self, **kwargs):
        """Add section data in context."""
        context = super(MyIncidentView, self).get_context_data(**kwargs)
        context['my_incident'] = 'my_incident'
        return context


class OpenTaskView(BaseLoginRequired, ListView):
    model = Incident
    template_name = "task_list.html"
    context_object_name = 'tasks_list'
    # paginate_by = 20

    def get_queryset(self):
        tasks_list = Task.objects.filter(status='open')
        return tasks_list

    def get_context_data(self, **kwargs):
        """Add section data in context."""
        context = super(OpenTaskView, self).get_context_data(**kwargs)
        context['open_task'] = 'open_task'
        return context


class MyTaskView(BaseLoginRequired, ListView):
    model = Incident
    template_name = "task_list.html"
    context_object_name = 'tasks_list'
    # paginate_by = 20

    def get_queryset(self):
        tasks_list = Task.objects.filter(assigned_user=self.request.user)
        return tasks_list

    def get_context_data(self, **kwargs):
        """Add section data in context."""
        context = super(MyTaskView, self).get_context_data(**kwargs)
        context['my_task'] = 'my_task'
        return context


class RecentTaskChartView(BaseLoginRequired, View):
    """Chart view."""

    template_name = 'chartcontainer.html'

    def get(self, request):
        """Generate recent task chart."""
        context = {}
        # status task
        context['open_task'] = Task.objects.filter(status='open')
        context['open_task_count'] = context['open_task'].count()
        context['inprogress_task'] = Task.objects.filter(status='in_progress')
        context['inprogress_task_count'] = context['inprogress_task'].count()
        context['close_task'] = Task.objects.filter(status='complete')
        context['close_task_count'] = context['close_task'].count()
        # status incident
        context['open_incident_count'] = Incident.objects.filter(status='open').count()
        context['closed_incident_count'] = Incident.objects.filter(status='closed').count()
        context['inprogress_incident_count'] = Incident.objects.filter(status='in_progress').count()
        context['pending_incident_count'] = Incident.objects.filter(status='pending').count()
        # active user
        context['active_user_count'] =  User.objects.filter(is_active=True).count()
        context['inactive_user_count'] =  User.objects.filter(is_active=False).count()
        # recent task
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        date_from= pytz.UTC.localize(date_from)
        context['recent_task'] = Task.objects.filter(created_on=date_from)
        context['recent_open_task_count'] = context['recent_task'].filter(status='open').count()
        context['recent_inprogress_task_count'] = context['recent_task'].filter(status='in_progress').count()
        context['recent_close_task_count'] = context['close_task'].filter(status='complete').count()
        # Incidents chart ( per sector )
        all_sector = Sector.objects.all()
        context['sector_count'] = []
        for sector in all_sector:
            count = Incident.objects.filter(sector=sector).count()
            context['sector_count'].append({sector.name:count})
        return render(request, self.template_name, context=context)


class CalendarView(BaseLoginRequired, ListView):
    model = Incident
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + datetime.timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class BlogCreateView(BaseLoginRequired, FormView):
    """Create blog."""

    template_name = 'create_blog.html'
    form_class = BlogForm

    def form_valid(self, form):
        """Save data."""
        form_obj = BlogForm(self.request.POST)
        if form_obj.is_valid():
            form_obj.instance.user = self.request.user
            form_obj.save()
        return HttpResponseRedirect(reverse('blog-list'))


class BlogUpdateView(BaseLoginRequired, UpdateView):
    """Update blog view."""

    model = Blog
    template_name = 'update_blog.html'
    form_class = BlogForm
    success_url = None

    # def get_context_data(self, **kwargs):
    #     context = super(BlogUpdateView,self).get_context_data(**kwargs)
    #     return context

    def post(self, request, pk):
        blog_obj=Blog.objects.get(pk=pk)
        form_obj = BlogForm(request.POST, instance=blog_obj)
        if form_obj.is_valid():
            form_obj.instance.user = self.request.user
            form_obj.save()
            return HttpResponseRedirect(reverse('blog-list'))
        else:
            ctx = {
                'form': form_obj,
            }
            return render(request, self.template_name, ctx)


class BlogListView(BaseLoginRequired, ListView):
    model = Blog
    template_name = "blog_list.html"
    context_object_name = 'blog_list'


def export_incident_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="incident.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Incidents')
    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['subject', 'description', 'status', 'category', 'sector', 'affectedunit', 'assigned_user']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Incident.objects.all().values_list('subject', 'description', 'status', 'category', 'sector', 'affectedunit', 'assigned_user')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_task_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="task.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Tasks')
    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['task_subject', 'assigned_user', 'attachment', 'status', 'incident', 'due_date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Task.objects.all().values_list('task_subject', 'assigned_user', 'attachment', 'status', 'incident', 'due_date')
    # import pdb;pdb.set_trace()
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 5:
                due_date = row[col_num].strftime("%d/%m/%y")
                ws.write(row_num, col_num, due_date, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
