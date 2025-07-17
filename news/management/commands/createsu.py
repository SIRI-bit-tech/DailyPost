from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = "Create or update superuser with password from env"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        first_name = os.environ.get("DJANGO_SUPERUSER_FIRST_NAME", "")
        last_name = os.environ.get("DJANGO_SUPERUSER_LAST_NAME", "")

        if not username or not email or not password:
            self.stdout.write(self.style.ERROR("Missing superuser env vars"))
            return

        user, created = User.objects.get_or_create(username=username, defaults={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "is_superuser": True,
            "is_staff": True,
        })
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        if created:
            self.stdout.write(self.style.SUCCESS(f"Superuser {username} created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser {username} updated")) 