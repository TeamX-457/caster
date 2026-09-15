from django.db import models

from apps.accounts.models import School, Student, Teacher


class StudyGuide(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='study_guides')
    subject = models.CharField(max_length=100)
    topic = models.CharField(max_length=150)
    title = models.CharField(max_length=200)
    content = models.TextField(help_text='The core study material for this guide.')
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='study_guides')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject}: {self.title}'


class LearningActivity(models.Model):
    class ActivityType(models.TextChoices):
        READING = 'reading', 'Reading'
        PRACTICE = 'practice', 'Practice'
        VIDEO = 'video', 'Video'
        DISCUSSION = 'discussion', 'Discussion'

    study_guide = models.ForeignKey(StudyGuide, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ActivityType.choices, default=ActivityType.READING)
    title = models.CharField(max_length=200)
    instructions = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class StudentProgress(models.Model):
    class Status(models.TextChoices):
        ASSIGNED = 'assigned', 'Assigned'
        IN_PROGRESS = 'in_progress', 'In progress'
        COMPLETED = 'completed', 'Completed'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='progress_records')
    study_guide = models.ForeignKey(StudyGuide, on_delete=models.CASCADE, related_name='progress_records')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ASSIGNED)
    assigned_by = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'study_guide')
        ordering = ['-assigned_at']
        verbose_name_plural = 'Student progress records'

    def __str__(self):
        return f'{self.student} - {self.study_guide} ({self.status})'
