from django.db import models
from django.conf import settings  # 기업 계정도 AUTH_USER_MODEL 기반이라고 가정

class JobPost(models.Model):
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.employer.username})"
