"""
Grant and Application models for GrantBridge.
Represents grant opportunities and application tracking.
"""

from django.db import models
import uuid


class Grant(models.Model):
    """
    Grant model representing funding opportunities.
    Includes embedding support for AI-powered matching.
    """
    
    STATUS_CHOICES = [
        ('opportunity', 'Opportunity'),
        ('reviewing', 'Reviewing'),
        ('drafting', 'Drafting'),
        ('submitted', 'Submitted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500, db_index=True)
    organization = models.CharField(
        max_length=255,
        help_text="Funding organization name"
    )
    
    # Financial Information
    funding_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Total funding amount available"
    )
    min_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum funding amount"
    )
    max_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum funding amount"
    )
    
    # Grant Details
    description = models.TextField(help_text="Detailed grant description")
    requirements = models.TextField(help_text="Grant requirements and criteria")
    eligibility = models.JSONField(
        default=list,
        help_text="List of eligibility criteria",
        blank=True
    )
    
    # Categorization
    tags = models.JSONField(
        default=list,
        help_text="Grant tags/keywords for filtering",
        blank=True
    )
    categories = models.JSONField(
        default=list,
        help_text="Grant categories (e.g., ['education', 'health'])",
        blank=True
    )
    
    # Important Dates
    deadline = models.DateTimeField(
        db_index=True,
        help_text="Application deadline"
    )
    announcement_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When grant was announced"
    )
    award_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Expected award date"
    )
    
    # Source Information
    source = models.CharField(
        max_length=255,
        help_text="Source of grant (e.g., grants.gov, foundation website)"
    )
    source_url = models.URLField(
        blank=True,
        help_text="URL to original grant posting"
    )
    external_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        help_text="External identifier from source system"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='opportunity',
        db_index=True
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether grant is currently accepting applications"
    )
    
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
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'grants'
        verbose_name = 'Grant'
        verbose_name_plural = 'Grants'
        indexes = [
            models.Index(fields=['deadline', 'is_active']),
            models.Index(fields=['funding_amount']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]
        ordering = ['-deadline']
    
    def __str__(self):
        return self.title
    
    @property
    def is_expired(self):
        """Check if grant deadline has passed."""
        from django.utils import timezone
        return self.deadline < timezone.now()
    
    @property
    def days_until_deadline(self):
        """Calculate days remaining until deadline."""
        from django.utils import timezone
        if self.is_expired:
            return 0
        delta = self.deadline - timezone.now()
        return delta.days
    
    @property
    def proposal_count(self):
        """Return number of proposals for this grant."""
        return self.proposals.count()
    
    @property
    def application_count(self):
        """Return number of applications for this grant."""
        return self.applications.count()
    
    @property
    def needs_embedding_update(self):
        """Check if embedding needs to be updated."""
        if not self.embedding_vector:
            return True
        if not self.last_embedding_update:
            return True
        return self.updated_at > self.last_embedding_update


class Application(models.Model):
    """
    Application model for tracking grant applications.
    Links grants with organizations and proposals.
    """
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    grant = models.ForeignKey(
        Grant,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='applications'
    )
    proposal = models.OneToOneField(
        'proposals.Proposal',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='application'
    )
    
    # Status and Progress
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        db_index=True
    )
    progress = models.IntegerField(
        default=0,
        help_text="Completion percentage (0-100)"
    )
    
    # Submission Information
    submitted_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When application was submitted"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'applications'
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['grant', 'status']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
        unique_together = [['grant', 'organization']]
    
    def __str__(self):
        return f"{self.organization.name} - {self.grant.title}"
    
    @property
    def is_submitted(self):
        """Check if application has been submitted."""
        return self.status != 'draft'
    
    @property
    def days_since_submission(self):
        """Calculate days since submission."""
        if not self.submitted_date:
            return None
        from django.utils import timezone
        delta = timezone.now() - self.submitted_date
        return delta.days

# Made with Bob
