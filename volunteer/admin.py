from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event, EventParticipation, EventReport


class CustomUserAdmin(UserAdmin):
    """Admin settings for the custom user model"""
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'age', 'volunteer_hours', 'is_admin', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Volunteer Info', {'fields': ('age', 'phone_number', 'address', 'skills', 'volunteer_hours', 'is_admin')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Volunteer Info', {'fields': ('age', 'phone_number', 'address', 'skills', 'is_admin')}),
    )


class EventParticipationInline(admin.TabularInline):
    """Inline admin for event participants"""
    model = EventParticipation
    extra = 0


class EventAdmin(admin.ModelAdmin):
    """Admin settings for Event model"""
    list_display = ['name', 'status', 'category', 'start_time', 'end_time', 'location', 'volunteer_hours', 'participant_count']
    list_filter = ['status', 'category', 'start_time']
    search_fields = ['name', 'description', 'location']
    inlines = [EventParticipationInline]


class EventReportAdmin(admin.ModelAdmin):
    """Admin settings for EventReport model"""
    list_display = ['event', 'actual_participants', 'report_date', 'created_by']
    search_fields = ['event__name', 'report_content']


# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventReport, EventReportAdmin) 