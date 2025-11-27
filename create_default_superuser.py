from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Creates a default superuser if not present."

    def handle(self, *args, **kwargs):
        User = get_user_model()

        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@gmail.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "1234")

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Superuser already exists: {email}"))
            return

        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser created: {email}"))
