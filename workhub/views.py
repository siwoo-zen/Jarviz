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
from django.core.exceptions import PermissionDenied
from workhub.models import CATEGORY_CHOICES, EXPERIENCE_CHOICES, EDUCATION_CHOICES, LOCATION_CHOICES


# 메인 대시보드
def main_dashboard(request):
    resume = None
    job_posts = None
    total_views = None
    applicant_count = None
    recommended_resumes = []
    recommended_jobs = []
    recent_applications = []
    is_employer = False

    if request.user.is_authenticated:
        is_employer = getattr(request.user, 'is_company', False)
        if is_employer:
            job_posts = JobPost.objects.filter(employer=request.user)
            total_views = job_posts.aggregate(Sum('views'))['views__sum'] or 0
            applicant_count = job_posts.aggregate(Sum('applicants'))['applicants__sum'] or 0

            for job in job_posts:
                job.applicant_count = job.applications.count()

            if job_posts.exists():
                recent_job = job_posts.first()
                job_tech_ids = set(recent_job.tech_stack.values_list('id', flat=True))

                recommended_resumes = Resume.objects.filter(
                    tech_stack__in=recent_job.tech_stack.all()
                ).distinct()[:3]

                for resume in recommended_resumes:
                    resume_tech_ids = set(resume.tech_stack.values_list('id', flat=True))
                    resume.matched_tech_count = len(job_tech_ids & resume_tech_ids)
        else:
            resume = Resume.objects.filter(user=request.user).first()

            # 추천 공고
            if resume:
                recommended_jobs = JobPost.objects.filter(
                    tech_stack__in=resume.tech_stack.all()
                ).distinct().order_by('-created_at')[:3]

            # 최근 지원 내역
            recent_applications = Application.objects.filter(
            user=request.user
            ).select_related('job').order_by('-applied_at')[:3]


    return render(request, 'main.html', {
        'resume': resume,
        'is_employer': is_employer,
        'job_posts': job_posts,
        'applicant_count': applicant_count,
        'total_views': total_views,
        'recommended_resumes': recommended_resumes,
        'recommended_jobs': recommended_jobs,
        'recent_applications': recent_applications,
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

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user != obj.employer:  # 본인이 보면 조회수 증가 제외
            obj.views = F('views') + 1
            obj.save(update_fields=['views'])
            obj.refresh_from_db(fields=['views'])
        return obj


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
        queryset = JobPost.objects.order_by('-created_at')

        # 필터링용 GET 파라미터 추출
        category = self.request.GET.get('category')
        experience = self.request.GET.get('experience')
        education = self.request.GET.get('education')
        location = self.request.GET.get('location')
        favorite = self.request.GET.get('favorite')

        # 조건별 필터링
        if category:
            queryset = queryset.filter(category=category)
        if experience:
            queryset = queryset.filter(experience=experience)
        if education:
            queryset = queryset.filter(education=education)
        if location:
            queryset = queryset.filter(location=location)
        if favorite and self.request.user.is_authenticated:
            scrap_ids = JobScrap.objects.filter(user=self.request.user).values_list('job_id', flat=True)
            queryset = queryset.filter(id__in=scrap_ids)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 기존 스크랩 공고 ID 유지
        if self.request.user.is_authenticated:
            scraps = JobScrap.objects.filter(user=self.request.user)
            context['scrapped_jobs'] = [s.job.id for s in scraps]
        else:
            context['scrapped_jobs'] = []

        # 드롭다운 선택값 유지
        context['selected'] = {
            'category': self.request.GET.get('category', ''),
            'experience': self.request.GET.get('experience', ''),
            'education': self.request.GET.get('education', ''),
            'location': self.request.GET.get('location', ''),
            'favorite': self.request.GET.get('favorite', ''),
        }

        # 드롭다운 메뉴용 choice 전달
        context['CATEGORY_CHOICES'] = CATEGORY_CHOICES
        context['EXPERIENCE_CHOICES'] = EXPERIENCE_CHOICES
        context['EDUCATION_CHOICES'] = EDUCATION_CHOICES
        context['LOCATION_CHOICES'] = LOCATION_CHOICES

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
        # 이력서를 모두 보여줌 (지원 여부 관계없이)
        return Resume.objects.filter(
            tech_stack__in=job.tech_stack.all()
        ).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = get_object_or_404(JobPost, pk=self.kwargs['pk'], employer=self.request.user)
        resumes = context['recommended_resumes']

        job_techs = set(job.tech_stack.values_list('id', flat=True))

        for resume in resumes:
            resume_techs = set(resume.tech_stack.values_list('id', flat=True))
            resume.matched_tech_count = len(resume_techs & job_techs)

        context['job'] = job  # 템플릿에서 job.title 등 사용 가능
        return context

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_company


class JobApplicantsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = JobPost
    template_name = 'company/job_applicants.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applications = self.object.applications.select_related('user', 'resume')

        job_tech_ids = set(self.object.tech_stack.values_list('id', flat=True))  # 기준 공고의 기술 스택

        # 기술 스택 일치 수 계산
        for app in applications:
            resume_tech_ids = set(app.resume.tech_stack.values_list('id', flat=True))
            app.matched_tech_count = len(job_tech_ids & resume_tech_ids)  # 동적으로 속성 추가

        context['applications'] = applications
        return context

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.employer and self.request.user.is_company


class CompanyViewResumeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Resume
    template_name = 'company/view_resume_detail.html'
    context_object_name = 'resume'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()

        # 이력서를 제출한 지원 기록들 (해당 기업 공고에만 필터)
        applications = resume.applications.filter(job__employer=self.request.user)
        context['applications'] = applications  # 여기에 여러 JobPost가 연결됨
        return context
