"""Create a superuser from environment variables if it does not exist."""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a default superuser using DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD"

    def handle(self, *args, **options):
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not email or not password:
            self.stdout.write(self.style.WARNING("DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD must be set"))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Superuser with email {email} already exists"))
            return

        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser {email} created successfully"))
