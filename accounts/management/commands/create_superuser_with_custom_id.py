import random
import string
import re
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = 'Creates a superuser with a unique custom_id and validates inputs'

    def generate_custom_id(self):
        """Generates a unique custom_id"""
        return 'admin' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    def validate_email(self, email):
        """Validates the email format."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError("Invalid email format.")
        return email

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Ask for the necessary fields
        username = input('Username (required): ').strip()
        while not username:
            username = input(
                'Username is required. Please enter a username: ').strip()

        email = input('Email (required): ').strip()
        while not email:
            email = input('Email is required. Please enter an email: ').strip()
        try:
            email = self.validate_email(email)
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
            return

        first_name = input('First name (required): ').strip()
        while not first_name:
            first_name = input(
                'First name is required. Please enter a first name: ').strip()

        last_name = input('Last name (required): ').strip()
        while not last_name:
            last_name = input(
                'Last name is required. Please enter a last name: ').strip()

        # Generate a unique custom_id
        custom_id = self.generate_custom_id()

        # Create the user instance
        user = User(
            username=username,
            email=email,
            custom_id=custom_id,  # Automatically generated
            first_name=first_name,
            last_name=last_name,
            is_staff=True,  # Staff users have admin privileges
            is_superuser=True  # Superuser privileges
        )

        # Set password
        password = input('Password (required): ').strip()
        while not password:
            password = input(
                'Password is required. Please enter a password: ').strip()

        password_confirm = input('Confirm password (required): ').strip()
        while password != password_confirm:
            password_confirm = input(
                'Passwords do not match. Please confirm your password again: ').strip()

        user.set_password(password)  # Ensure the password is hashed

        # Save the user
        try:
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f'Superuser created successfully with custom_id: {custom_id}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
