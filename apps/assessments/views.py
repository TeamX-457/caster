from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from apps.study.models import StudyGuide

from .forms import AssessmentForm, ChoiceFormSet, QuestionForm
from .models import Assessment, AssessmentAttempt, Choice, Question, StudentAnswer


class AssessmentCreateView(LoginRequiredMixin, CreateView):
    form_class = AssessmentForm
    template_name = 'assessments/assessment_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_teacher:
            return redirect('accounts:dashboard')
        self.study_guide = get_object_or_404(
            StudyGuide, pk=kwargs['pk'], created_by=request.user.teacher_profile
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.study_guide = self.study_guide
        form.instance.created_by = self.request.user.teacher_profile
        messages.success(self.request, 'Assessment created. Now add some questions.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['study_guide'] = self.study_guide
        return context

    def get_success_url(self):
        return reverse('assessments:assessment_detail', args=[self.object.pk])


class AssessmentDetailView(LoginRequiredMixin, DetailView):
    model = Assessment
    template_name = 'assessments/assessment_detail.html'
    context_object_name = 'assessment'

    def get_queryset(self):
        return Assessment.objects.filter(study_guide__school=self.request.user.school)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_student:
            context['attempt'] = AssessmentAttempt.objects.filter(
                student=self.request.user.student_profile, assessment=self.object
            ).order_by('-completed_at').first()
        return context


@login_required
def add_question(request, pk):
    if not request.user.is_teacher:
        return redirect('accounts:dashboard')
    assessment = get_object_or_404(Assessment, pk=pk, created_by=request.user.teacher_profile)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)
        if question_form.is_valid() and formset.is_valid():
            choice_data = [f for f in formset.cleaned_data if f.get('text')]
            if not choice_data:
                messages.error(request, 'Add at least one choice.')
            elif not any(f['is_correct'] for f in choice_data):
                messages.error(request, 'Mark at least one choice as correct.')
            else:
                question = question_form.save(commit=False)
                question.assessment = assessment
                question.order = assessment.questions.count()
                question.save()
                for choice in choice_data:
                    Choice.objects.create(
                        question=question, text=choice['text'], is_correct=choice['is_correct']
                    )
                messages.success(request, 'Question added.')
                return redirect('assessments:assessment_detail', pk=assessment.pk)
    else:
        question_form = QuestionForm()
        formset = ChoiceFormSet()

    return render(request, 'assessments/question_form.html', {
        'assessment': assessment,
        'question_form': question_form,
        'formset': formset,
    })


class AssessmentTakeView(LoginRequiredMixin, View):
    template_name = 'assessments/assessment_take.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_student:
            return redirect('accounts:dashboard')
        self.assessment = get_object_or_404(
            Assessment, pk=kwargs['pk'], study_guide__school=request.user.school
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        questions = self.assessment.questions.prefetch_related('choices')
        return render(request, self.template_name, {'assessment': self.assessment, 'questions': questions})

    def post(self, request, *args, **kwargs):
        questions = list(self.assessment.questions.prefetch_related('choices'))
        score = 0
        answers = []
        for question in questions:
            choice_id = request.POST.get(f'question_{question.id}')
            selected_choice = None
            if choice_id:
                selected_choice = question.choices.filter(pk=choice_id).first()
                if selected_choice and selected_choice.is_correct:
                    score += 1
            answers.append((question, selected_choice))

        attempt = AssessmentAttempt.objects.create(
            student=request.user.student_profile,
            assessment=self.assessment,
            score=score,
            total=len(questions),
        )
        StudentAnswer.objects.bulk_create([
            StudentAnswer(attempt=attempt, question=question, selected_choice=choice)
            for question, choice in answers
        ])
        return redirect('assessments:attempt_result', pk=attempt.pk)


class AttemptResultView(LoginRequiredMixin, DetailView):
    model = AssessmentAttempt
    template_name = 'assessments/attempt_result.html'
    context_object_name = 'attempt'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_student:
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return AssessmentAttempt.objects.filter(student=self.request.user.student_profile)
