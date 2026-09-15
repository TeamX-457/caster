from django.contrib.auth.models import AbstractUser
from django.db import models


class School(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'
        SCHOOL_ADMIN = 'school_admin', 'School Administrator'

    role = models.CharField(max_length=20, choices=Role.choices, blank=True)
    school = models.ForeignKey(
        School, null=True, blank=True, on_delete=models.SET_NULL, related_name='members'
    )

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_school_admin(self):
        return self.role == self.Role.SCHOOL_ADMIN


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    subject_specialty = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def school(self):
        return self.user.school


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    grade_level = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def school(self):
        return self.user.school
