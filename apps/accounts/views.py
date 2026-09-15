from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView

from apps.assessments.models import AssessmentAttempt
from apps.study.models import StudentProgress, StudyGuide

from .forms import AddTeacherForm, SchoolSignupForm, StudentSignupForm, StyledAuthenticationForm
from .models import Student, Teacher


class LoginView(DjangoLoginView):
    template_name = 'accounts/login.html'
    authentication_form = StyledAuthenticationForm


class StudentSignupView(FormView):
    template_name = 'accounts/signup_student.html'
    form_class = StudentSignupForm
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class SchoolSignupView(FormView):
    template_name = 'accounts/signup_school.html'
    form_class = SchoolSignupForm
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class AddTeacherView(LoginRequiredMixin, FormView):
    template_name = 'accounts/add_teacher.html'
    form_class = AddTeacherForm
    success_url = reverse_lazy('accounts:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_school_admin:
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Teacher account created.')
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.is_student:
            return self._student_dashboard(request)
        if user.is_teacher:
            return self._teacher_dashboard(request)
        if user.is_school_admin:
            return self._school_admin_dashboard(request)
        return redirect('marketing:home')

    def _student_dashboard(self, request):
        student = request.user.student_profile
        progress_records = StudentProgress.objects.filter(student=student).select_related('study_guide')
        attempts = AssessmentAttempt.objects.filter(student=student).select_related('assessment')
        return self._render(request, 'accounts/dashboard_student.html', {
            'progress_records': progress_records,
            'attempts': attempts,
        })

    def _teacher_dashboard(self, request):
        teacher = request.user.teacher_profile
        study_guides = StudyGuide.objects.filter(created_by=teacher)
        students = Student.objects.filter(user__school=request.user.school).select_related('user')
        return self._render(request, 'accounts/dashboard_teacher.html', {
            'study_guides': study_guides,
            'students': students,
        })

    def _school_admin_dashboard(self, request):
        school = request.user.school
        teachers = Teacher.objects.filter(user__school=school).select_related('user')
        students = Student.objects.filter(user__school=school).select_related('user')
        study_guides = StudyGuide.objects.filter(school=school)
        return self._render(request, 'accounts/dashboard_school_admin.html', {
            'school': school,
            'teachers': teachers,
            'students': students,
            'study_guides': study_guides,
        })

    def _render(self, request, template_name, context):
        return render(request, template_name, context)
