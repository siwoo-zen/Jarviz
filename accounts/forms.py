from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccount, EmployerAccount


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'password1', 'password2']


class CustomEmployerCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = EmployerAccount
        fields = [
            'username', 'email', 'password1', 'password2',
            'company_name', 'contact_person', 'phone_number', 'company_website',
        ]

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('password1')
        pw2 = cleaned_data.get('password2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
