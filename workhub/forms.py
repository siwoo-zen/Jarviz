from django import forms
from .models import Resume, JobPost

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
