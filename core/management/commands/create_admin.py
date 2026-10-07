import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update the admin user from environment variables"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("ADMIN_USERNAME")
        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        if not username or not password:
            self.stdout.write("Admin environment variables are not set.")
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email or "",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        # Force update all fields and permissions
        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        # Force set password
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created new admin user '{username}'.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Updated password and permissions for admin user '{username}'.")
            )