from .models import JobPost

def latest_job_post(request):
    if request.user.is_authenticated and request.user.is_company:
        latest_job = JobPost.objects.filter(employer=request.user).order_by('-created_at').first()
        return {'latest_job': latest_job}
    return {}
