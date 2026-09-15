from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import School, Student, Teacher, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ['username', 'email', 'role', 'school', 'is_staff']
    list_filter = ['role', 'school', 'is_staff', 'is_superuser']
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('CASTER profile', {'fields': ('role', 'school')}),
    )


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'created_at']
    search_fields = ['name']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'school', 'subject_specialty']
    search_fields = ['user__username', 'user__email']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'school', 'grade_level']
    search_fields = ['user__username', 'user__email']
