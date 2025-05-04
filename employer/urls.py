from django.urls import path, include
from .views import JobPostCreateView

urlpatterns = [
    path('employer/', include('employer.urls')),
    path('job/create/', JobPostCreateView.as_view(), name='job_create'),
]
