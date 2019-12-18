from django import forms
# from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from .models import *

AssignedUser =   tuple([('---------','---------')]+ [(user, user) for user in User.objects.filter(is_active=True).exclude(is_superuser=True)])

class IncidentForm(forms.ModelForm):
    """Incident model form."""

    assigned_user = forms.ChoiceField(choices=AssignedUser)

    # def clean_assigned_user(self):
    #     """Check password1 and password2 match or not."""
    #     import pdb;pdb.set_trace()
    #     assigned_user = self.cleaned_data.get('assigned_user')
    #     user_obj = User.objects.filter(username=assigned_user)
    #     # if password1 and password2 and password1 != password2:
    #     #     raise forms.ValidationError("Password does not match.")
    #     return assigned_user

    class Meta:
        model = Incident
        # fields = "__all__"
        exclude = ()

# TaskFormSet = inlineformset_factory(Incident, Task)
# RelatedipFormSet = inlineformset_factory(Incident, Related_ip)
# RelateddomainFormSet = inlineformset_factory(Incident, Related_domain)

    # def __init__(self, *args, **kwargs):
    #     super(IncidentForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_tag = True
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.label_class = 'col-md-3 create-label'
    #     self.helper.field_class = 'col-md-9'
    #     self.helper.layout = Layout(
    #         Div(
    #             Field('subject'),
    #             Field('category'),
    #             Field('sector'),
    #             Field('affectedunit'),
    #             Field('timestamp'),
    #             Field('description'),
    #             Field('status'),
    #             Field('assigned_user'),
    #             Field('attachment'),
    #             Fieldset(_('Add Tasks'),
    #                 Formset('titles')),
    #             # Fieldset(_('Add Ip'),
    #             #     Formset('relatedip')),
    #             # Fieldset(_('Add Domain'),
    #             #     Formset('domain')),
    #             HTML("<br>"),
    #             ButtonHolder(Submit('submit', _('save'))),
    #             )
    #         )


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ()

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
