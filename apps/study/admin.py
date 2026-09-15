from django.contrib import admin

from .models import LearningActivity, StudentProgress, StudyGuide


class LearningActivityInline(admin.TabularInline):
    model = LearningActivity
    extra = 0


@admin.register(StudyGuide)
class StudyGuideAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'topic', 'school', 'created_by', 'created_at']
    list_filter = ['school', 'subject']
    search_fields = ['title', 'subject', 'topic']
    inlines = [LearningActivityInline]


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'study_guide', 'status', 'assigned_at', 'completed_at']
    list_filter = ['status']
