from django.urls import path

from . import views
from . import ajax

urlpatterns = [
    path('create-incident/', views.CreateIncidentView.as_view(), name='create-incident'),
    path('edit-incident/<int:pk>/', views.UpdateIncidentView.as_view(), name='edit-incident'),
    path('delete-incident/<int:pk>/', ajax.DeleteIncidentView.as_view(), name='delete-incident'),
    path('incident-detail/<int:pk>/', views.IncidentDetailView.as_view(), name='incident-detail'),
    path('list-incident/', views.ListIncidentView.as_view(), name='list-incident'),
    path('open-incident/', views.OpenIncidentView.as_view(), name='open-incident'),
    path('closed-incident/', views.ClosedIncidentView.as_view(), name='closed-incident'),
    path('inprogress-incident/', views.InprogressIncidentView.as_view(), name='inprogress-incident'),
    path('pending-incident/', views.PendingIncidentView.as_view(), name='pending-incident'),
    path('latest-incident/', views.LatestIncidentView.as_view(), name='latest-incident'),
    path('my-incident/', views.MyIncidentView.as_view(), name='my-incident'),
    path('open-task/', views.OpenTaskView.as_view(), name='open-task'),
    path('my-task/', views.MyTaskView.as_view(), name='my-task'),
    path('add-comment/', ajax.AddCommentView.as_view(), name='add-comment'),
    path('recent-task-chart/', views.RecentTaskChartView.as_view(), name='recent-task-chart'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('blog-create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('blog-update/<int:pk>/', views.BlogUpdateView.as_view(), name='blog-update'),
    path('blog-list/', views.BlogListView.as_view(), name='blog-list'),
    path('blog-delete/<int:pk>/', ajax.BlogDeleteView.as_view(), name='blog-delete'),
    path('export/xls/', views.export_incident_xls, name='export_incident_xls'),
]
