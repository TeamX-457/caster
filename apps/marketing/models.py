from django.db import models


class WaitlistSignup(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'
        SCHOOL_ADMIN = 'school_admin', 'School Administrator'
        PARENT = 'parent', 'Parent / Guardian'
        OTHER = 'other', 'Other'

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    school_name = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Waitlist signup'
        verbose_name_plural = 'Waitlist signups'

    def __str__(self):
        return f'{self.full_name} <{self.email}>'
