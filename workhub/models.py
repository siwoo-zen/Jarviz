from django.db import models
from django.contrib.auth import get_user_model

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
