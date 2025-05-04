from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'content', 'uploaded_file', 'category', 'tech_stack']
        widgets = {
            'tech_stack': forms.CheckboxSelectMultiple,
            'category': forms.Select, 
        }
