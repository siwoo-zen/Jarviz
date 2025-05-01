from django.urls import path
from . import views
from .views import main_dashboard

urlpatterns = [
    path('', main_dashboard, name='home'),  
]
