"""Create a superuser from environment variables if it does not exist."""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Ensures a superuser exists using DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD"

    def handle(self, *args, **options):
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not email or not password:
            self.stdout.write(self.style.WARNING("DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD must be set"))
            return

        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if user:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password(password)
            user.save(update_fields=["is_staff", "is_superuser", "is_active", "password"])
            self.stdout.write(self.style.SUCCESS(f"Superuser {email} updated with new credentials"))
            return

        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser {email} created successfully"))
