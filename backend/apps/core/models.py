"""
Core models including notifications.
"""

import uuid
from django.db import models
from django.utils import timezone


class Notification(models.Model):
    """
    Represents a notification for a user.

    Notifications are generated for various events such as:
    - New grant matches
    - Application status changes
    - Proposal updates
    - Deadline reminders
    - System announcements
    """

    # Notification Types
    GRANT_MATCH = "grant_match"
    APPLICATION_STATUS = "application_status"
    PROPOSAL_UPDATE = "proposal_update"
    DEADLINE_REMINDER = "deadline_reminder"
    SYSTEM_ANNOUNCEMENT = "system_announcement"

    NOTIFICATION_TYPE_CHOICES = [
        (GRANT_MATCH, "Grant Match"),
        (APPLICATION_STATUS, "Application Status"),
        (PROPOSAL_UPDATE, "Proposal Update"),
        (DEADLINE_REMINDER, "Deadline Reminder"),
        (SYSTEM_ANNOUNCEMENT, "System Announcement"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # User who receives the notification
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="User who receives this notification",
    )

    # Notification Details
    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPE_CHOICES,
        db_index=True,
        help_text="Type of notification",
    )

    title = models.CharField(max_length=255, help_text="Notification title")

    message = models.TextField(help_text="Notification message content")

    # Optional Related Objects
    related_grant = models.ForeignKey(
        "grants.Grant",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        help_text="Related grant if applicable",
    )

    related_proposal = models.ForeignKey(
        "proposals.Proposal",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        help_text="Related proposal if applicable",
    )

    related_application = models.ForeignKey(
        "grants.Application",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        help_text="Related application if applicable",
    )

    # Action URL (optional link for the notification)
    action_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="URL to navigate to when notification is clicked",
    )

    # Read Status
    is_read = models.BooleanField(
        default=False, db_index=True, help_text="Whether the notification has been read"
    )

    read_at = models.DateTimeField(
        null=True, blank=True, help_text="When the notification was read"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notifications"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["user", "-created_at"], name="notification_user_created_idx"
            ),
            models.Index(
                fields=["user", "is_read", "-created_at"],
                name="notification_user_read_idx",
            ),
            models.Index(
                fields=["notification_type", "-created_at"],
                name="notification_type_created_idx",
            ),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.title}"

    def mark_as_read(self):
        """Mark this notification as read."""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at", "updated_at"])

    def mark_as_unread(self):
        """Mark this notification as unread."""
        if self.is_read:
            self.is_read = False
            self.read_at = None
            self.save(update_fields=["is_read", "read_at", "updated_at"])

    @classmethod
    def create_grant_match_notification(cls, user, grant, match_score: float):
        """
        Create a notification for a new grant match.

        Args:
            user: User instance
            grant: Grant instance
            match_score: Match score (0-100)

        Returns:
            Notification instance
        """
        return cls.objects.create(
            user=user,
            notification_type=cls.GRANT_MATCH,
            title=f"New Grant Match: {grant.title}",
            message=(
                f"We found a {match_score:.0f}% match for your organization! "
                f"Check out this grant opportunity."
            ),
            related_grant=grant,
            action_url=f"/dashboard/grants/{grant.id}",
        )

    @classmethod
    def create_application_status_notification(cls, user, application, new_status: str):
        """
        Create a notification for application status change.

        Args:
            user: User instance
            application: Application instance
            new_status: New status value

        Returns:
            Notification instance
        """
        status_messages = {
            "draft": "Your application is in draft status.",
            "submitted": "Your application has been submitted!",
            "under_review": "Your application is under review.",
            "approved": "Congratulations! Your application was approved!",
            "rejected": "Your application was not approved this time.",
            "withdrawn": "Your application has been withdrawn.",
        }

        return cls.objects.create(
            user=user,
            notification_type=cls.APPLICATION_STATUS,
            title=f"Application Status Update: {application.grant.title}",
            message=status_messages.get(
                new_status, f"Application status changed to {new_status}"
            ),
            related_application=application,
            related_grant=application.grant,
            action_url=f"/dashboard/applications/{application.id}",
        )

    @classmethod
    def create_deadline_reminder_notification(cls, user, grant, days_remaining: int):
        """
        Create a notification for grant deadline reminder.

        Args:
            user: User instance
            grant: Grant instance
            days_remaining: Number of days until deadline

        Returns:
            Notification instance
        """
        if days_remaining == 1:
            message = (
                f"The deadline for {grant.title} is tomorrow! "
                f"Make sure to submit your application."
            )
        else:
            message = (
                f"The deadline for {grant.title} is in {days_remaining} "
                f"days. Don't miss this opportunity!"
            )

        return cls.objects.create(
            user=user,
            notification_type=cls.DEADLINE_REMINDER,
            title=f"Deadline Reminder: {grant.title}",
            message=message,
            related_grant=grant,
            action_url=f"/dashboard/grants/{grant.id}",
        )

    @classmethod
    def get_unread_count(cls, user) -> int:
        """
        Get the count of unread notifications for a user.

        Args:
            user: User instance

        Returns:
            Count of unread notifications
        """
        return cls.objects.filter(user=user, is_read=False).count()

    @classmethod
    def mark_all_as_read(cls, user):
        """
        Mark all notifications as read for a user.

        Args:
            user: User instance

        Returns:
            Number of notifications marked as read
        """
        return cls.objects.filter(user=user, is_read=False).update(
            is_read=True, read_at=timezone.now()
        )


# Made with Bob
