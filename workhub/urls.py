from django.urls import path
from .views import ResumeCreateView, ResumeUpdateView, ResumeListView, ResumeDetailView
from workhub.views import main_dashboard

app_name = 'workhub'

urlpatterns = [
    path('', main_dashboard, name='home'),
    path('resume/create/', ResumeCreateView.as_view(), name='resume_create'),
    path('resume/<int:pk>/edit/', ResumeUpdateView.as_view(), name='resume_edit'),
    path('resume/list/', ResumeListView.as_view(), name='resume_list'),
    path('resume/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),
    #path('jobs/create/', JobCreateView.as_view(), name='job_create'),

]
