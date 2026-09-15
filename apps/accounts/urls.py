from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/student/', views.StudentSignupView.as_view(), name='signup_student'),
    path('signup/school/', views.SchoolSignupView.as_view(), name='signup_school'),
    path('teachers/add/', views.AddTeacherView.as_view(), name='add_teacher'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
