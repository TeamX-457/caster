from django.contrib import admin

from .models import WaitlistSignup


@admin.register(WaitlistSignup)
class WaitlistSignupAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'role', 'school_name', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['full_name', 'email', 'school_name']
    readonly_fields = ['created_at']
