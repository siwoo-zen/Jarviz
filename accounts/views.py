from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('registration_pending')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        print("✅ 회원가입 성공, 이메일 전송 시작")
        send_verification_email(self.request, user)
        return response


def send_verification_email(request, user):
    print(f"📨 인증 메일 전송 대상: {user.email}")
    current_site = get_current_site(request)
    subject = 'Jarviz 이메일 인증'

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verification_link = f"http://{current_site.domain}/accounts/activate/{uid}/{token}/"

    message = render_to_string('accounts/email_verification.html', {
        'user': user,
        'verification_link': verification_link,
    })

    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = "html"
    email.send()

def activate_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/activation_success.html')
    else:
        return render(request, 'accounts/activation_failed.html')
