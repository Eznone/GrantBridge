"""
Proposal model for GrantBridge.
Represents grant proposals with AI generation metadata.
"""

from django.db import models
import uuid


class Proposal(models.Model):
    """
    Proposal model representing grant proposals.
    Includes AI generation metadata and versioning support.
    """
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    grant = models.ForeignKey(
        'grants.Grant',
        on_delete=models.CASCADE,
        related_name='proposals',
        help_text="Grant this proposal is for"
    )
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='proposals',
        help_text="Organization submitting the proposal"
    )
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_proposals',
        help_text="User who created this proposal"
    )
    
    # Content
    title = models.CharField(max_length=500)
    content = models.TextField(
        help_text="Proposal content in markdown/HTML format"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        db_index=True
    )
    
    # AI Generation Metadata
    ai_generated = models.BooleanField(
        default=False,
        help_text="Whether this proposal was AI-generated"
    )
    ai_model_used = models.CharField(
        max_length=100,
        blank=True,
        help_text="AI model used for generation (e.g., 'watsonx.ai/granite-13b')"
    )
    generation_metadata = models.JSONField(
        null=True,
        blank=True,
        help_text="Metadata about AI generation (tokens used, confidence, etc.)"
    )
    
    # Submission Information
    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When proposal was submitted"
    )
    submission_method = models.CharField(
        max_length=100,
        blank=True,
        help_text="How proposal was submitted (e.g., 'email', 'portal')"
    )
    
    # Versioning
    version = models.IntegerField(
        default=1,
        help_text="Version number of this proposal"
    )
    parent_version = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='versions',
        help_text="Previous version of this proposal"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'proposals'
        verbose_name = 'Proposal'
        verbose_name_plural = 'Proposals'
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['grant', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} - {self.organization.name}"
    
    @property
    def is_submitted(self):
        """Check if proposal has been submitted."""
        return self.status in ['submitted', 'approved', 'rejected']
    
    @property
    def is_editable(self):
        """Check if proposal can be edited."""
        return self.status in ['draft', 'review']
    
    @property
    def word_count(self):
        """Calculate approximate word count of content."""
        if not self.content:
            return 0
        # Simple word count (can be improved)
        return len(self.content.split())
    
    @property
    def has_versions(self):
        """Check if this proposal has previous versions."""
        return self.parent_version is not None
    
    @property
    def version_count(self):
        """Count total versions of this proposal."""
        count = 1
        current = self.parent_version
        while current:
            count += 1
            current = current.parent_version
        return count
    
    def create_new_version(self):
        """Create a new version of this proposal."""
        new_proposal = Proposal.objects.create(
            grant=self.grant,
            organization=self.organization,
            created_by=self.created_by,
            title=self.title,
            content=self.content,
            status='draft',
            ai_generated=self.ai_generated,
            ai_model_used=self.ai_model_used,
            version=self.version + 1,
            parent_version=self
        )
        return new_proposal
    
    @property
    def ai_generation_summary(self):
        """Get summary of AI generation metadata."""
        if not self.ai_generated or not self.generation_metadata:
            return None
        
        return {
            'model': self.ai_model_used,
            'tokens_used': self.generation_metadata.get('tokensUsed', 0),
            'confidence': self.generation_metadata.get('confidence', 0),
            'generated_at': self.generation_metadata.get('generatedAt', ''),
        }

# Made with Bob
