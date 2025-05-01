from django.urls import path
from django.contrib.auth.views import LoginView
from .views import CustomLoginView, RegisterView, activate_user
from django.views.generic import TemplateView


urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'), 
    path('activate/<uidb64>/<token>/', activate_user, name='activate'), 
    path('register/complete/', TemplateView.as_view(
        template_name='accounts/registration_pending.html'
    ), name='registration_pending'),
]