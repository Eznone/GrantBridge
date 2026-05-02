"""
Django admin configuration for organizations app.
"""

from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin interface for Organization model."""
    
    list_display = [
        'name', 
        'type', 
        'city', 
        'state', 
        'is_verified', 
        'user_count',
        'created_at'
    ]
    list_filter = ['is_verified', 'type', 'state', 'created_at']
    search_fields = ['name', 'email', 'ein', 'city']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'type', 'ein', 'is_verified')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Organization Details', {
            'fields': ('mission', 'description', 'goals', 'categories', 'historical_projects')
        }),
        ('Financial Information', {
            'fields': ('year_founded', 'annual_budget', 'funding_needs')
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
    
    def user_count(self, obj):
        """Display user count in list view."""
        return obj.user_count
    user_count.short_description = 'Users'

# Made with Bob
