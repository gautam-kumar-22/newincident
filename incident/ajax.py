from django.views.generic.edit import DeleteView
from django.http.response import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse_lazy
from users_profile.views import BaseLoginRequired
from .models import *


class DeleteIncidentView(DeleteView):
    model = Incident
    success_url = reverse_lazy('list-incident')


class AddCommentView(View):

    def post(self, request, *args, **kwargs):
        if request.POST.get('incident_id', None):
            incident_obj = Incident.objects.get(id=request.POST.get('incident_id'))
        comment_obj = Comment.objects.create(comment=request.POST.get('comment_text'),incident=incident_obj, user=request.user)
        return render(request, "new_comment.html", {'comment_obj': comment_obj})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog-list')


class GetAffectedUnit(BaseLoginRequired):
    """Get affected unit of selected sector."""

    template_name = '_affectedunits.html'

    def get(self, request):
        sector_id = request.GET.get('sector_id', None)
        if sector_id:
            affected_units = AffectedUnit.objects.filter(sector__id=sector_id)
        else:
            affected_units = AffectedUnit.objects.all()
        rendered_data = render_to_string(self.template_name, {'affected_units': affected_units}, request=request)
        return JsonResponse({'rendered_data': rendered_data})
