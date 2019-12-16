from django.views.generic.edit import DeleteView
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse_lazy
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
