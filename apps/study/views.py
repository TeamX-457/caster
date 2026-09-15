from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from .forms import AssignStudyGuideForm, LearningActivityForm, StudyGuideForm
from .models import StudentProgress, StudyGuide


class TeacherRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_teacher:
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)


class StudyGuideCreateView(TeacherRequiredMixin, CreateView):
    model = StudyGuide
    form_class = StudyGuideForm
    template_name = 'study/studyguide_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user.teacher_profile
        form.instance.school = self.request.user.school
        response = super().form_valid(form)
        messages.success(self.request, 'Study guide created.')
        return response

    def get_success_url(self):
        return reverse('study:studyguide_detail', args=[self.object.pk])


class StudyGuideDetailView(LoginRequiredMixin, DetailView):
    model = StudyGuide
    template_name = 'study/studyguide_detail.html'
    context_object_name = 'study_guide'

    def get_queryset(self):
        return StudyGuide.objects.filter(school=self.request.user.school)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_student:
            progress, created = StudentProgress.objects.get_or_create(
                student=request.user.student_profile,
                study_guide=self.object,
            )
            if progress.status == StudentProgress.Status.ASSIGNED:
                progress.status = StudentProgress.Status.IN_PROGRESS
                progress.started_at = timezone.now()
                progress.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_student:
            context['progress'] = StudentProgress.objects.get(
                student=self.request.user.student_profile,
                study_guide=self.object,
            )
        return context


class AddActivityView(LoginRequiredMixin, CreateView):
    form_class = LearningActivityForm
    template_name = 'study/activity_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_teacher:
            return redirect('accounts:dashboard')
        self.study_guide = get_object_or_404(
            StudyGuide, pk=kwargs['pk'], created_by=request.user.teacher_profile
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.study_guide = self.study_guide
        messages.success(self.request, 'Activity added.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['study_guide'] = self.study_guide
        return context

    def get_success_url(self):
        return reverse('study:studyguide_detail', args=[self.study_guide.pk])


class AssignStudyGuideView(LoginRequiredMixin, View):
    template_name = 'study/assign_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_teacher:
            return redirect('accounts:dashboard')
        self.study_guide = get_object_or_404(
            StudyGuide, pk=kwargs['pk'], school=request.user.school
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = AssignStudyGuideForm(school=request.user.school)
        return render(request, self.template_name, {'form': form, 'study_guide': self.study_guide})

    def post(self, request, *args, **kwargs):
        form = AssignStudyGuideForm(request.POST, school=request.user.school)
        if form.is_valid():
            for student in form.cleaned_data['students']:
                StudentProgress.objects.get_or_create(
                    student=student,
                    study_guide=self.study_guide,
                    defaults={'assigned_by': request.user.teacher_profile},
                )
            messages.success(request, 'Study guide assigned.')
            return redirect('study:studyguide_detail', pk=self.study_guide.pk)
        return render(request, self.template_name, {'form': form, 'study_guide': self.study_guide})


class MarkCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_student:
            return redirect('accounts:dashboard')
        study_guide = get_object_or_404(StudyGuide, pk=pk)
        progress = get_object_or_404(
            StudentProgress, student=request.user.student_profile, study_guide=study_guide
        )
        progress.status = StudentProgress.Status.COMPLETED
        progress.completed_at = timezone.now()
        progress.save()
        messages.success(request, 'Marked as completed.')
        return redirect('study:studyguide_detail', pk=pk)
