from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomLoginView, RegisterView, activate_user, EmployerLoginView
from django.views.generic import TemplateView
from .views import EmployerRegisterView
from workhub.views import main_dashboard 

app_name = 'accounts'

urlpatterns = [
    path('', main_dashboard, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'), 
    path('activate/<uidb64>/<token>/', activate_user, name='activate'), 
    path('register/complete/', TemplateView.as_view(
        template_name='accounts/registration_pending.html'
    ), name='registration_pending'),
    path('employer/login/', EmployerLoginView.as_view(), name='employer_login'),
    path('employer/register/', EmployerRegisterView.as_view(), name='employer_register'),
    path('logout/', LogoutView.as_view(next_page='workhub:home'), name='logout'),
]