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
from django.db.models import F
from django.db.models import Sum


# 메인 대시보드
def main_dashboard(request):
    resume = None
    job_posts = None
    total_views = None
    applicant_count = None
    is_employer = False

    if request.user.is_authenticated:
        is_employer = getattr(request.user, 'is_company', False)
        if is_employer:
            job_posts = JobPost.objects.filter(employer=request.user)
            total_views = job_posts.aggregate(Sum('views'))['views__sum'] or 0
            applicant_count = job_posts.aggregate(Sum('applicants'))['applicants__sum'] or 0
        else:
            resume = Resume.objects.filter(user=request.user).first()

    return render(request, 'main.html', {
        'resume': resume,
        'is_employer': is_employer,
        'job_posts': job_posts,
        'applicant_count': applicant_count,
        'total_views': total_views,
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
    success_url = reverse_lazy('workhub:job_list')

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
    success_url = reverse_lazy('workhub:job_list')  #  여기서 목록으로 이동
    context_object_name = 'job'

    def form_valid(self, form):
        messages.success(self.request, "공고가 성공적으로 수정되었습니다.")  # 메시지 추가
        return super().form_valid(form)

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
    
    def get_object(self, queryset=None):  #조회수 증가 로직
        obj = super().get_object(queryset)
        JobPost.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        return obj

class JobPostDetailView(DetailView):
    model = JobPost
    template_name = 'company/job_detail.html'
    context_object_name = 'job'