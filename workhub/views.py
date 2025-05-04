from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django import forms
from .forms import ResumeForm, JobPostForm
from .models import Resume, JobPost
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# 메인 대시보드
def main_dashboard(request):
    is_employer = False
    resume = None

    if request.user.is_authenticated:
        is_employer = getattr(request.user, 'is_company', False)
        if not is_employer:
            resume = Resume.objects.filter(user=request.user).first()

    return render(request, 'main.html', {
        'resume': resume,
        'is_employer': is_employer
    })



# 이력서 생성 (클래스형 뷰)
class ResumeCreateView(CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'user/resume_create.html'
    success_url = reverse_lazy('workhub:home')

    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.user = self.request.user
        resume.save()
        return super().form_valid(form)


# 이력서 수정 (클래스형 뷰)
class ResumeUpdateView(UpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'user/resume_edit.html'
    success_url = reverse_lazy('workhub:resume_list')
    
    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.user = self.request.user
        resume.save()
        form.save_m2m()
        messages.success(self.request, "이력서가 성공적으로 수정되었습니다.")
        return redirect('workhub:resume_list')

class ResumeListView(ListView):
    model = Resume
    template_name = 'user/resume_list.html'
    context_object_name = 'resumes'

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user).order_by('-created_at')
    

class ResumeDetailView(DetailView):
    model = Resume
    template_name = 'user/resume_detail.html'
    context_object_name = 'resume'

# 채용공고 생성 (기업 전용)
class JobPostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'company/job_create.html'
    success_url = reverse_lazy('workhub:home')

    def form_valid(self, form):
        form.instance.employer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_company


# 채용공고 수정
class JobPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'company/job_edit.html'
    success_url = reverse_lazy('workhub:home')

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_company


# 채용공고 리스트
class JobPostListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = JobPost
    template_name = 'company/job_list.html'
    context_object_name = 'job_posts'

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user).order_by('-created_at')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_company
