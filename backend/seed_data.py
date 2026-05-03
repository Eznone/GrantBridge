"""
Database seed script for GrantBridge.
Creates sample data for development and testing.

Usage:
    python seed_data.py
"""

import os
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from django.utils import timezone
from apps.authentication.models import User
from apps.organizations.models import Organization
from apps.grants.models import Grant, Application, SavedGrant
from apps.proposals.models import Proposal
from apps.matching.models import GrantMatch
from apps.core.models import Notification


def clear_data():
    """Clear existing data (use with caution!)"""
    print("Clearing existing data...")
    Notification.objects.all().delete()
    GrantMatch.objects.all().delete()
    SavedGrant.objects.all().delete()
    Application.objects.all().delete()
    Proposal.objects.all().delete()
    Grant.objects.all().delete()
    Organization.objects.all().delete()
    User.objects.all().delete()
    print("✓ Data cleared")


def create_users():
    """Create sample users"""
    print("\nCreating users...")

    users = []

    # Admin user
    admin = User.objects.create_superuser(
        email="admin@grantbridge.org",
        name="Admin User",
        password="admin123",
    )
    users.append(admin)
    print(f"✓ Created admin: {admin.email}")

    # Regular users
    user_data = [
        ("john@ngo.org", "John Doe", "password123"),
        ("jane@charity.org", "Jane Smith", "password123"),
        ("bob@foundation.org", "Bob Johnson", "password123"),
    ]

    for email, name, pwd in user_data:
        user = User.objects.create_user(
            email=email, name=name, password=pwd
        )
        users.append(user)
        print(f"✓ Created user: {email}")

    return users


def create_organizations(users):
    """Create sample organizations"""
    print("\nCreating organizations...")

    orgs = []

    org_data = [
        {
            "name": "Education for All Foundation",
            "description": "Dedicated to providing quality education to underserved communities",
            "mission": "Empowering communities through education",
            "website": "https://educationforall.org",
            "categories": ["education", "youth development", "community"],
            "goals": [
                "Increase literacy rates",
                "Provide scholarships",
                "Build schools",
            ],
            "user": users[1],
        },
        {
            "name": "Green Earth Initiative",
            "description": "Environmental conservation and sustainability programs",
            "mission": "Protecting our planet for future generations",
            "website": "https://greenearth.org",
            "categories": ["environment", "sustainability", "conservation"],
            "goals": ["Reduce carbon emissions", "Plant trees", "Clean water access"],
            "user": users[2],
        },
        {
            "name": "Health Access Network",
            "description": "Improving healthcare access in rural areas",
            "mission": "Healthcare for all, regardless of location",
            "website": "https://healthaccess.org",
            "categories": ["health", "medical", "rural development"],
            "goals": ["Mobile clinics", "Telemedicine", "Health education"],
            "user": users[3],
        },
    ]

    for data in org_data:
        user = data.pop("user")
        org = Organization.objects.create(**data)
        user.organization = org
        user.save()
        orgs.append(org)
        print(f"✓ Created organization: {org.name}")

    return orgs


def create_grants():
    """Create sample grants"""
    print("\nCreating grants...")

    grants = []
    now = timezone.now()

    grant_data = [
        {
            "title": "Community Education Grant 2026",
            "funder_name": "National Education Foundation",
            "funder_website": "https://nef.org",
            "funding_amount": Decimal("50000.00"),
            "currency": "USD",
            "description": "Supporting innovative education programs in underserved communities. Focus on literacy, STEM education, and teacher training.",
            "requirements": "Must serve communities with <60% literacy rate. Minimum 2 years operational history.",
            "eligibility": [
                "501(c)(3) status",
                "Education focus",
                "Serve underserved areas",
            ],
            "tags": ["education", "literacy", "STEM", "community"],
            "categories": ["education", "youth development"],
            "deadline": now + timedelta(days=45),
            "source": "grants.gov",
            "source_url": "https://grants.gov/12345",
        },
        {
            "title": "Environmental Conservation Fund",
            "funder_name": "Global Green Foundation",
            "funder_website": "https://globalgreen.org",
            "funding_amount": Decimal("75000.00"),
            "currency": "USD",
            "description": "Supporting projects that protect biodiversity and promote sustainable practices.",
            "requirements": "Demonstrated impact in environmental conservation. Partnership with local communities required.",
            "eligibility": [
                "Environmental focus",
                "Community engagement",
                "Measurable outcomes",
            ],
            "tags": ["environment", "conservation", "sustainability", "biodiversity"],
            "categories": ["environment", "conservation"],
            "deadline": now + timedelta(days=60),
            "source": "foundation website",
            "source_url": "https://globalgreen.org/grants",
        },
        {
            "title": "Rural Healthcare Access Initiative",
            "funder_name": "Health Equity Fund",
            "funder_website": "https://healthequity.org",
            "funding_amount": Decimal("100000.00"),
            "currency": "USD",
            "description": "Expanding healthcare access in rural and remote areas through innovative delivery models.",
            "requirements": "Must serve rural populations. Experience with telemedicine or mobile clinics preferred.",
            "eligibility": [
                "Healthcare focus",
                "Rural service area",
                "Licensed providers",
            ],
            "tags": ["health", "rural", "telemedicine", "access"],
            "categories": ["health", "rural development"],
            "deadline": now + timedelta(days=30),
            "source": "foundation database",
            "source_url": "https://healthequity.org/apply",
        },
        {
            "title": "Youth Leadership Development Program",
            "funder_name": "Future Leaders Foundation",
            "funder_website": "https://futureleaders.org",
            "funding_amount": Decimal("35000.00"),
            "currency": "USD",
            "description": "Supporting programs that develop leadership skills in young people aged 13-25.",
            "requirements": "Program must include mentorship component. Serve minimum 50 youth annually.",
            "eligibility": [
                "Youth focus",
                "Leadership development",
                "Mentorship program",
            ],
            "tags": ["youth", "leadership", "mentorship", "development"],
            "categories": ["youth development", "education"],
            "deadline": now + timedelta(days=90),
            "source": "grants.gov",
            "source_url": "https://grants.gov/67890",
        },
        {
            "title": "Clean Water Access Project",
            "funder_name": "Water for Life Initiative",
            "funder_website": "https://waterforlife.org",
            "funding_amount": Decimal("150000.00"),
            "currency": "USD",
            "description": "Infrastructure projects providing clean water access to communities in need.",
            "requirements": "Engineering expertise required. Community partnership essential.",
            "eligibility": [
                "Water/sanitation focus",
                "Engineering capacity",
                "Community engagement",
            ],
            "tags": ["water", "infrastructure", "sanitation", "community"],
            "categories": ["environment", "infrastructure", "health"],
            "deadline": now + timedelta(days=120),
            "source": "foundation website",
            "source_url": "https://waterforlife.org/grants",
        },
    ]

    for data in grant_data:
        grant = Grant.objects.create(**data)
        grants.append(grant)
        print(f"✓ Created grant: {grant.title}")

    return grants


def create_proposals(orgs, grants):
    """Create sample proposals"""
    print("\nCreating proposals...")

    proposals = []

    # Education org proposal for education grant
    proposal1 = Proposal.objects.create(
        grant=grants[0],
        organization=orgs[0],
        created_by=orgs[0].users.first(),
        title="Literacy Program for Rural Communities",
        content="## Executive Summary\n\nOur literacy program will serve 500 students...",
        status="draft",
        ai_generated=False,
        version=1,
    )
    proposals.append(proposal1)
    print(f"✓ Created proposal: {proposal1.title}")

    # Environment org proposal for conservation grant
    proposal2 = Proposal.objects.create(
        grant=grants[1],
        organization=orgs[1],
        created_by=orgs[1].users.first(),
        title="Biodiversity Protection Initiative",
        content="## Project Description\n\nWe will protect 1000 acres of forest...",
        status="submitted",
        ai_generated=True,
        ai_model_used="watsonx.ai/granite-13b",
        submitted_at=timezone.now() - timedelta(days=5),
        version=1,
    )
    proposals.append(proposal2)
    print(f"✓ Created proposal: {proposal2.title}")

    return proposals


def create_applications(orgs, grants):
    """Create sample applications"""
    print("\nCreating applications...")

    applications = []

    app1 = Application.objects.create(
        grant=grants[0], organization=orgs[0], status="draft", progress=25
    )
    applications.append(app1)

    app2 = Application.objects.create(
        grant=grants[1],
        organization=orgs[1],
        status="submitted",
        submitted_date=timezone.now() - timedelta(days=10),
        progress=100,
    )
    applications.append(app2)

    print(f"✓ Created {len(applications)} applications")
    return applications


def create_matches(orgs, grants):
    """Create sample grant matches"""
    print("\nCreating grant matches...")

    matches = []

    # Education org matches
    match1 = GrantMatch.objects.create(
        organization=orgs[0],
        grant=grants[0],
        match_score=92.5,
        match_reasons=[
            "Perfect alignment with education focus",
            "Serves target demographic",
            "Funding amount matches needs",
        ],
        recommended_actions=[
            "Review requirements in detail",
            "Start drafting proposal",
            "Contact program officer",
        ],
        algorithm_version="1.0.0",
    )
    matches.append(match1)

    # Environment org matches
    match2 = GrantMatch.objects.create(
        organization=orgs[1],
        grant=grants[1],
        match_score=88.0,
        match_reasons=[
            "Strong environmental focus alignment",
            "Previous conservation experience",
            "Community engagement model",
        ],
        recommended_actions=[
            "Prepare project timeline",
            "Gather community letters of support",
            "Review budget requirements",
        ],
        algorithm_version="1.0.0",
    )
    matches.append(match2)

    print(f"✓ Created {len(matches)} grant matches")
    return matches


def create_notifications(users):
    """Create sample notifications"""
    print("\nCreating notifications...")

    notifications = []

    for user in users[1:]:  # Skip admin
        # Grant match notification
        notif1 = Notification.objects.create(
            user=user,
            notification_type=Notification.GRANT_MATCH,
            title="New Grant Match Found!",
            message="We found a 92% match for your organization.",
            action_url="/dashboard/matches",
        )
        notifications.append(notif1)

        # Deadline reminder
        notif2 = Notification.objects.create(
            user=user,
            notification_type=Notification.DEADLINE_REMINDER,
            title="Grant Deadline Approaching",
            message="The Community Education Grant deadline is in 45 days.",
            action_url="/dashboard/grants",
            is_read=True,
        )
        notifications.append(notif2)

    print(f"✓ Created {len(notifications)} notifications")
    return notifications


def main():
    """Main seed function"""
    print("=" * 60)
    print("GrantBridge Database Seeding")
    print("=" * 60)

    # Ask for confirmation
    response = input("\nThis will clear existing data. Continue? (yes/no): ")
    if response.lower() != "yes":
        print("Aborted.")
        return

    # Clear and seed
    clear_data()
    users = create_users()
    orgs = create_organizations(users)
    grants = create_grants()
    proposals = create_proposals(orgs, grants)
    applications = create_applications(orgs, grants)
    matches = create_matches(orgs, grants)
    notifications = create_notifications(users)

    print("\n" + "=" * 60)
    print("✓ Database seeding complete!")
    print("=" * 60)
    print(f"\nCreated:")
    print(f"  - {len(users)} users")
    print(f"  - {len(orgs)} organizations")
    print(f"  - {len(grants)} grants")
    print(f"  - {len(proposals)} proposals")
    print(f"  - {len(applications)} applications")
    print(f"  - {len(matches)} grant matches")
    print(f"  - {len(notifications)} notifications")
    print(f"\nLogin credentials:")
    print(f"  Admin: admin@grantbridge.org / admin123")
    print(f"  User: john@ngo.org / password123")
    print(f"  User: jane@charity.org / password123")
    print(f"  User: bob@foundation.org / password123")
    print("\n")


if __name__ == "__main__":
    main()

# Made with Bob
