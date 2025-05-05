# forms.py
from django import forms
from .models import Resume, JobPost, Application

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'content', 'uploaded_file', 'category', 'tech_stack']
        widgets = {
            'tech_stack': forms.CheckboxSelectMultiple,
            'category': forms.Select, 
        }

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'category', 'location', 'salary', 'deadline', 'tech_stack']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'category': forms.Select(),
            'description': forms.Textarea(attrs={'rows': 5}),
            'tech_stack': forms.CheckboxSelectMultiple,
        }

class ApplyJobForm(forms.ModelForm):  # 💡 이름 변경
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
