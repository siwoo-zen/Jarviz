from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_verification_email(request, user):
    subject = "Jarviz 이메일 인증"
    uid = user.pk
    verify_url = request.build_absolute_uri(
        reverse("activate", kwargs={"user_id": uid})
    )
    message = f"{user.username}님, 아래 링크를 눌러 이메일 인증을 완료해주세요:\n\n{verify_url}"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
