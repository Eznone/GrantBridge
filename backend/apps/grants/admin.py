"""
Django admin configuration for grants app.
"""

from django.contrib import admin
from .models import Grant, Application


@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
    """Admin interface for Grant model."""
    
    list_display = [
        'title',
        'funder_name',
        'funding_amount',
        'deadline',
        'status',
        'is_active',
        'days_until_deadline',
        'created_at'
    ]
    list_filter = ['status', 'is_active', 'source', 'created_at', 'deadline']
    search_fields = ['title', 'funder_name', 'description', 'external_id']
    ordering = ['-deadline']
    date_hierarchy = 'deadline'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'funder_name', 'status', 'is_active')
        }),
        ('Financial Details', {
            'fields': ('funding_amount', 'min_amount', 'max_amount')
        }),
        ('Grant Details', {
            'fields': ('description', 'requirements', 'eligibility', 'tags', 'categories')
        }),
        ('Important Dates', {
            'fields': ('deadline', 'announcement_date', 'award_date')
        }),
        ('Source Information', {
            'fields': ('source', 'source_url', 'external_id')
        }),
        ('AI/Matching', {
            'fields': ('embedding_vector', 'last_embedding_update'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_embedding_update']
    
    def days_until_deadline(self, obj):
        """Display days until deadline."""
        if obj.is_expired:
            return "Expired"
        return f"{obj.days_until_deadline} days"
    days_until_deadline.short_description = 'Time Remaining'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin interface for Application model."""
    
    list_display = [
        'organization',
        'grant',
        'status',
        'progress',
        'submitted_date',
        'created_at'
    ]
    list_filter = ['status', 'created_at', 'submitted_date']
    search_fields = ['organization__name', 'grant__title']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Application Details', {
            'fields': ('grant', 'organization', 'proposal')
        }),
        ('Status', {
            'fields': ('status', 'progress', 'submitted_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('grant', 'organization', 'proposal')

# Made with Bob
