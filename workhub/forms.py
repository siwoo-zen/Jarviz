# forms.py
from django import forms
from .models import Resume, JobPost, Application
import datetime
from django.utils import timezone

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'content', 'uploaded_file', 'category', 'tech_stack', 'experience', 'education', 'preferred_location']
        widgets = {
            'tech_stack': forms.CheckboxSelectMultiple,
            'category': forms.Select, 
        }

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'category', 'location', 'salary', 'deadline', 'tech_stack', 'education', 'experience']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'category': forms.Select(),
            'location': forms.Select(), 
            'education': forms.Select(),  
            'experience': forms.Select(),  
            'description': forms.Textarea(attrs={'rows': 5}),
            'tech_stack': forms.CheckboxSelectMultiple,
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # 모집 마감일 디폴트 1개월+
            self.initial['deadline'] = (timezone.now() + datetime.timedelta(days=30)).date()

class ApplyJobForm(forms.ModelForm): 
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'placeholder': '간단한 자기소개나 포부를 입력하세요.',
                'rows': 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['resume'].queryset = Resume.objects.filter(user=user)
