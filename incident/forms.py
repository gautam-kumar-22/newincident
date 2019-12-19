from django import forms
# from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from .models import *
import datetime

class IncidentForm(forms.ModelForm):
    """Incident model form."""

    timestamp = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M:%S'])

    def __init__(self, *args, **kwargs):
        super(IncidentForm, self).__init__(*args, **kwargs)
        dt = datetime.datetime.now()
        self.fields['assigned_user'].queryset = self.fields['assigned_user'].queryset.filter(is_active=True).exclude(is_superuser=True)
        self.fields['timestamp'].initial = dt.strftime('%d/%m/%Y %H:%M:%S')
        # self.fields['timestamp'].required = True

    # def clean_timestamp(self):
    #     import pdb;pdb.set_trace()
    #     data = self.cleaned_data['timestamp']
    #     return data

    class Meta:
        model = Incident
        fields = ('subject', 'category', 'timestamp','sector','affectedunit','description','status','assigned_user','attachment',)
        # exclude = ()


class TaskForm(forms.ModelForm):

    # due_date = forms.DateTimeField(input_formats=['%d/%m/%Y'])

    # def clean_due_date(self):
    #     import pdb;pdb.set_trace()
    #     data = self.cleaned_data['due_date']
    #     return data

    class Meta:
        model = Task
        fields = ('task_subject', 'assigned_user', 'due_date', 'status', 'attachment',)

TaskFormSet = inlineformset_factory(
    Incident, Task, form=TaskForm,
    fields=['task_subject', 'assigned_user', 'due_date', 'status', 'attachment'], extra=1, can_delete=True
    )


class RelatedipForm(forms.ModelForm):

    class Meta:
        model = Related_ip
        exclude = ()

RelatedipFormSet = inlineformset_factory(
    Incident, Related_ip, form=RelatedipForm,
    fields=['name'], extra=1, can_delete=True)


class RelateddomainForm(forms.ModelForm):

    class Meta:
        model = Related_domain
        exclude = ()

RelateddomainFormSet = inlineformset_factory(
    Incident, Related_domain, form=RelateddomainForm,
    fields=['name'], extra=1, can_delete=True)


class BlogForm(forms.ModelForm):
    """Blog model form."""

    class Meta:
        model = Blog
        exclude = ()
