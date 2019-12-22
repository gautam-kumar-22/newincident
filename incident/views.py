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
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.db import transaction
from django.utils.safestring import mark_safe

from .models import *
from .utils import Calendar
from .forms import IncidentForm, BlogForm, RelatedipFormSet, RelateddomainFormSet, TaskFormSet
from users_profile.views import BaseLoginRequired

import calendar
import datetime
import pytz
import xlwt


class CreateIncidentView(CreateView):
    template_name = 'incident_add.html'
    model = Incident
    form_class = IncidentForm
    success_url = None

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        task_form = TaskFormSet()
        relatedip_form = RelatedipFormSet()
        relateddomain_form = RelateddomainFormSet()
        return self.render_to_response(self.get_context_data(
            form=form, task_form=task_form, relatedip_form=relatedip_form, relateddomain_form=relateddomain_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        task_form = TaskFormSet(self.request.POST, self.request.FILES)
        relatedip_form = RelatedipFormSet(self.request.POST)
        relateddomain_form = RelateddomainFormSet(self.request.POST)
        if (form.is_valid() and task_form.is_valid() and relatedip_form.is_valid() and relateddomain_form.is_valid()):
            return self.form_valid(form, task_form, relatedip_form, relateddomain_form)
        else:
            return self.form_invalid(form, task_form, relatedip_form, relateddomain_form)

    def form_valid(self, form, task_form, relatedip_form, relateddomain_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        task_form.instance = self.object
        task_form.save()
        relatedip_form.instance = self.object
        relatedip_form.save()
        relateddomain_form.instance = self.object
        relateddomain_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, task_form, relatedip_form, relateddomain_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(self.get_context_data(
            form=form, task_form=task_form, relatedip_form=relatedip_form, relateddomain_form=relateddomain_form))

    def get_success_url(self):
        return reverse_lazy('list-incident')


class UpdateIncidentView(UpdateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'edit_incident.html'
    success_url = None

    def get_success_url(self):
        return reverse_lazy('list-incident')

    def get_context_data(self, **kwargs):
        context = super(UpdateIncidentView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['task_form'] = TaskFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['relatedip_form'] = RelatedipFormSet(self.request.POST, instance=self.object)
            context['relateddomain_form'] = RelateddomainFormSet(self.request.POST, instance=self.object)
        else:
            context['task_form'] = TaskFormSet(instance=self.object)
            context['relatedip_form'] = RelatedipFormSet(instance=self.object)
            context['relateddomain_form'] = RelateddomainFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        task_form = context['task_form']
        relatedip_form = context['relatedip_form']
        relateddomain_form = context['relateddomain_form']
        if task_form.is_valid() and relatedip_form.is_valid() and relateddomain_form.is_valid():
            self.object = form.save()
            task_form.instance = self.object
            task_form.save()
            relatedip_form.instance = self.object
            relatedip_form.save()
            relateddomain_form.instance = self.object
            relateddomain_form.save()
        return super(UpdateIncidentView, self).form_valid(form)


class ListIncidentView(BaseLoginRequired, ListView):
    model = Incident
    template_name = "incident_list.html"
    context_object_name = 'incidents_list'

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
        context['related_ips'] = Related_ip.objects.filter(incident=context['incident'])
        context['related_domains'] = Related_domain.objects.filter(incident=context['incident'])
        context['all_comment'] = Comment.objects.filter(incident=context['incident']).order_by('created_on')
        return context


class OpenIncidentView(BaseLoginRequired, ListView):
    model = Incident
    template_name = "incident_list.html"
    context_object_name = 'incidents_list'

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


class AllTaskView(BaseLoginRequired, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = 'tasks_list'

    def get_context_data(self, **kwargs):
        """Add section data in context."""
        context = super(AllTaskView, self).get_context_data(**kwargs)
        context['all_task'] = 'all_task'
        return context


class OpenTaskView(BaseLoginRequired, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = 'tasks_list'

    def get_queryset(self):
        tasks_list = Task.objects.filter(status='open')
        return tasks_list

    def get_context_data(self, **kwargs):
        """Add section data in context."""
        context = super(OpenTaskView, self).get_context_data(**kwargs)
        context['open_task'] = 'open_task'
        return context


class MyTaskView(BaseLoginRequired, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = 'tasks_list'

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
        context['recent_close_task_count'] = context['recent_task'].filter(status='complete').count()
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
