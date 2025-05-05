from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django import forms
from .forms import ResumeForm, JobPostForm
from .models import Resume, JobPost, JobScrap, Application
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F, Sum
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest

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


# 이력서 뷰
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


# 기업 전용 공고
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


class JobPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'company/job_edit.html'
    success_url = reverse_lazy('workhub:job_list')
    context_object_name = 'job'

    def form_valid(self, form):
        messages.success(self.request, "공고가 성공적으로 수정되었습니다.")
        return super().form_valid(form)

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_company


class JobPostListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = JobPost
    template_name = 'company/job_list.html'
    context_object_name = 'job_posts'

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user).order_by('-created_at')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_company


class JobPostDetailView(DetailView):
    model = JobPost
    template_name = 'company/job_detail.html'
    context_object_name = 'job'


# 사용자 공고 지원
class ApplyJobView(LoginRequiredMixin, View):
    def post(self, request, pk):
        job = JobPost.objects.get(pk=pk)
        resume_id = request.POST.get('resume_id')
        resume = Resume.objects.get(pk=resume_id, user=request.user)

        if Application.objects.filter(user=request.user, job=job).exists():
            messages.warning(request, "이미 이 공고에 지원하셨습니다.")
        else:
            Application.objects.create(user=request.user, job=job, resume=resume)
            job.applicants += 1
            job.save()
            messages.success(request, "지원이 완료되었습니다!")

        return redirect('workhub:public_job_detail', pk=pk)


# 사용자용 공고 리스트/상세
class PublicJobListView(ListView):
    model = JobPost
    template_name = 'user/job_list_user_show.html'
    context_object_name = 'job_posts'
    paginate_by = 10

    def get_queryset(self):
        return JobPost.objects.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            scraps = JobScrap.objects.filter(user=self.request.user)
            context['scrapped_jobs'] = [s.job.id for s in scraps]
        else:
            context['scrapped_jobs'] = []
        return context


class PublicJobDetailView(DetailView):
    model = JobPost
    template_name = 'user/public_job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['resumes'] = Resume.objects.filter(user=self.request.user)
        else:
            context['resumes'] = []
        return context


# 스크랩 기능
class ToggleScrapView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            job = JobPost.objects.get(pk=pk)
        except JobPost.DoesNotExist:
            return HttpResponseBadRequest("잘못된 요청입니다.")

        scrap, created = JobScrap.objects.get_or_create(user=request.user, job=job)

        if not created:
            scrap.delete()
            return JsonResponse({'scrapped': False})
        return JsonResponse({'scrapped': True})

class MyApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'user/my_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.select_related('job', 'resume').filter(user=self.request.user).order_by('-applied_at')
    
class RecommendedResumeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Resume
    template_name = 'company/recommended_resumes.html'
    context_object_name = 'recommended_resumes'

    def get_queryset(self):
        job = get_object_or_404(JobPost, pk=self.kwargs['pk'], employer=self.request.user)
        return Resume.objects.filter(
            tech_stack__in=job.tech_stack.all()
        ).exclude(
            applications__job=job
        ).distinct()

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_company
