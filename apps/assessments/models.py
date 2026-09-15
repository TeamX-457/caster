from django.db import models

from apps.accounts.models import Student, Teacher
from apps.study.models import StudyGuide


class Assessment(models.Model):
    study_guide = models.ForeignKey(StudyGuide, on_delete=models.CASCADE, related_name='assessments')
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assessments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Question(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class AssessmentAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assessment_attempts')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f'{self.student} - {self.assessment} ({self.score}/{self.total})'

    @property
    def percent(self):
        if not self.total:
            return 0
        return round(self.score / self.total * 100)


class StudentAnswer(models.Model):
    attempt = models.ForeignKey(AssessmentAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='+')
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, related_name='+')
