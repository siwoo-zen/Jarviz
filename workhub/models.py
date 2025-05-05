from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()

CATEGORY_CHOICES = [
    ('dev', '개발'),
    ('design', '디자인'),
    ('plan', '기획'),
    ('qa', 'QA'),
    ('pm', 'PM'),
    ('etc', '기타'),
]

class TechStack(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    uploaded_file = models.FileField(upload_to='resumes/%Y/%m/%d/', blank=True, null=True)
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tech_stack = models.ManyToManyField(TechStack, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"
    

class JobPost(models.Model):
    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_company': True},
        related_name='workhub_jobposts'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    tech_stack = models.ManyToManyField(TechStack, blank=True)
    views = models.PositiveIntegerField(default=0)  # 조회수
    applicants = models.PositiveIntegerField(default=0)  # 지원자 수

    def __str__(self):
        return f"{self.title} - {self.employer.username}"

    class Meta:
        ordering = ['-created_at']

# 이력서 지원
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('reviewed', '검토중'),
        ('accepted', '합격'),
        ('rejected', '불합격'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    job = models.ForeignKey(
        JobPost,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('resume', 'job')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.user.username} → {self.job.title} ({self.get_status_display()})"

class JobScrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')  # 중복 저장 방지

    def __str__(self):
        return f"{self.user.username} → {self.job.title}"
    