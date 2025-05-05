from django.urls import path
from .views import ResumeCreateView, ResumeUpdateView, ResumeListView, ResumeDetailView, JobPostDetailView
from .views import JobPostCreateView, JobPostUpdateView, JobPostListView
from workhub.views import main_dashboard

app_name = 'workhub'

urlpatterns = [
    path('', main_dashboard, name='home'),
    path('resume/create/', ResumeCreateView.as_view(), name='resume_create'),
    path('resume/<int:pk>/edit/', ResumeUpdateView.as_view(), name='resume_edit'),
    path('resume/list/', ResumeListView.as_view(), name='resume_list'),
    path('resume/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),
    path('jobs/create/', JobPostCreateView.as_view(), name='job_create'),
    path('jobs/<int:pk>/edit/', JobPostUpdateView.as_view(), name='job_edit'),
    path('jobs/list/', JobPostListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', JobPostDetailView.as_view(), name='job_detail'),
]
