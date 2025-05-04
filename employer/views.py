from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import JobPost
from .forms import JobPostForm

class JobPostCreateView(LoginRequiredMixin, CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'employer/job_create.html'
    success_url = reverse_lazy('job_list')  # 목록 페이지로 이동할 예정 (이후 연결)

    def form_valid(self, form):
        form.instance.employer = self.request.user  # 현재 로그인한 기업 계정 연결
        return super().form_valid(form)
