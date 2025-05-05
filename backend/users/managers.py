# your_app_name/managers.py

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, username, first_name, last_name, password=None, **extra_fields):
        """
        Create and save a User with the given email, username, first_name, last_name and password.
        Email is the primary identifier, but username, first_name, and last_name are required.
        """
        # Ensure required fields are provided
        if not email:
            raise ValueError(_("The Email must be set"))
        if not username:
             raise ValueError(_("The Username must be set"))
        if not first_name:
             raise ValueError(_("The First Name must be set"))
        if not last_name:
             raise ValueError(_("The Last Name must be set"))

        # Normalize the email address
        email = self.normalize_email(email)

        # Create the user instance
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        # Set the password and save the user
        user.set_password(password)
        user.save(using=self._db) # Use self._db for multi-database support

        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email, username, first_name, last_name and password.
        Sets is_staff and is_superuser to True.
        """
        # Ensure superuser flags are set to True by default, and raise error if explicitly set to False
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True) # Superusers should be active

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        # Call the create_user method to handle validation and creation
        return self.create_user(
            email,
            username,
            first_name,
            last_name,
            password,
            **extra_fields
        )