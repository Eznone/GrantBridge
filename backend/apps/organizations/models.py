"""
Organization model for GrantBridge.
Represents NGO organizations that use the platform.
"""

from django.db import models
import uuid


class Organization(models.Model):
    """
    Organization model representing NGOs using GrantBridge.
    Includes mission, goals, categories, and AI embedding support.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=100, default='501(c)(3) Nonprofit')
    ein = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True,
        help_text='Employer Identification Number'
    )
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Address
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='USA')
    
    # Organization Details
    mission = models.TextField(help_text="Organization's mission statement")
    description = models.TextField(blank=True)
    
    # JSON fields for flexible data storage
    goals = models.JSONField(
        default=list,
        help_text="List of organizational goals",
        blank=True
    )
    categories = models.JSONField(
        default=list,
        help_text="Nonprofit categories/focus areas (e.g., ['education', 'health', 'environment'])",
        blank=True
    )
    historical_projects = models.JSONField(
        default=list,
        help_text="Past projects and achievements",
        blank=True
    )
    
    # Financial Information
    year_founded = models.IntegerField(null=True, blank=True)
    annual_budget = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Annual operating budget in USD"
    )
    funding_needs = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        help_text="Current funding needs in USD"
    )
    
    # Metadata
    is_verified = models.BooleanField(
        default=False,
        help_text="Whether organization has been verified by admin"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # AI/Matching Support
    embedding_vector = models.JSONField(
        null=True, 
        blank=True,
        help_text="Vector embedding for AI-powered matching"
    )
    last_embedding_update = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="When the embedding was last updated"
    )
    
    class Meta:
        db_table = 'organizations'
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_verified']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def user_count(self):
        """Return the number of users in this organization."""
        return self.users.count()
    
    @property
    def active_proposals_count(self):
        """Return the number of active proposals."""
        return self.proposals.filter(status__in=['draft', 'review']).count()
    
    @property
    def needs_embedding_update(self):
        """Check if embedding needs to be updated."""
        if not self.embedding_vector:
            return True
        if not self.last_embedding_update:
            return True
        # Update if organization was modified after last embedding update
        return self.updated_at > self.last_embedding_update

# Made with Bob
