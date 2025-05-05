from django.urls import path
from .views import ResumeCreateView, ResumeUpdateView, ResumeListView, ResumeDetailView, JobPostDetailView, MyApplicationsView
from .views import JobPostCreateView, JobPostUpdateView, JobPostListView, ApplyJobView, PublicJobListView, PublicJobDetailView, ToggleScrapView
from workhub.views import main_dashboard

app_name = 'workhub'


urlpatterns = [
    path('', main_dashboard, name='home'),

    # 이력서
    path('resume/create/', ResumeCreateView.as_view(), name='resume_create'),
    path('resume/<int:pk>/edit/', ResumeUpdateView.as_view(), name='resume_edit'),
    path('resume/list/', ResumeListView.as_view(), name='resume_list'),
    path('resume/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),

    # 기업 공고
    path('jobs/create/', JobPostCreateView.as_view(), name='job_create'),
    path('jobs/<int:pk>/edit/', JobPostUpdateView.as_view(), name='job_edit'),
    path('jobs/list/', JobPostListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', JobPostDetailView.as_view(), name='job_detail'),

    # 사용자 공개 공고
    path('jobs/', PublicJobListView.as_view(), name='public_job_list'),
    path('job/<int:pk>/', PublicJobDetailView.as_view(), name='public_job_detail'),

    # 사용자 기능
    path('job/<int:pk>/apply/', ApplyJobView.as_view(), name='apply_job'),
    path('job/<int:pk>/toggle-scrap/', ToggleScrapView.as_view(), name='toggle_scrap'),
    path('applications/', MyApplicationsView.as_view(), name='my_applications'),
]
