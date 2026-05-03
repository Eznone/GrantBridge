"""
Django admin configuration for proposals app.
"""

from django.contrib import admin
from .models import Proposal


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    """Admin interface for Proposal model."""
    
    list_display = [
        'title',
        'organization',
        'grant',
        'status',
        'ai_generated',
        'version',
        'word_count',
        'created_at'
    ]
    list_filter = ['status', 'ai_generated', 'created_at', 'submitted_at']
    search_fields = ['title', 'organization__name', 'grant__title', 'content']
    ordering = ['-updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'grant', 'organization', 'created_by', 'status')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('AI Generation', {
            'fields': ('ai_generated', 'ai_model_used', 'generation_metadata'),
            'classes': ('collapse',)
        }),
        ('Submission', {
            'fields': ('submitted_at', 'submission_method')
        }),
        ('Versioning', {
            'fields': ('version', 'parent_version'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def word_count(self, obj):
        """Display word count in list view."""
        return f"{obj.word_count} words"
    word_count.short_description = 'Length'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('grant', 'organization', 'created_by')

# Made with Bob
