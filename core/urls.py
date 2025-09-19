# core/urls.py

from django.urls import path
from . import views
from .views import CaseDeleteView
urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_case_view, name='create_case'),
    path('case/<int:case_id>/', views.case_detail_view, name='case_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/', views.profile_view, name='profile'),
    path('change_status/<int:case_id>/', views.change_case_status, name='change_case_status'),
    path('staff/dashboard/', views.staff_dashboard_view, name='staff_dashboard'),
    path('dashboard/', views.public_dashboard_view, name='public_dashboard'),
    path('delete/<int:case_id>/', CaseDeleteView.as_view(), name='case_delete'),



    
]