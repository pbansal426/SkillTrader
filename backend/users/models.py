# your_app_name/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager # Import your custom manager

class CustomUser(AbstractUser):
    """
    Custom User model where email is the primary identifier for authentication.
    Retains username, first_name, and last_name as required fields.
    """
    # The email field is already present in AbstractUser, but we explicitly define
    # it here to ensure unique=True and make it clear it's our primary login field.
    # AbstractUser's email field defaults to blank=True, null=True, max_length=254.
    # We override it to make it unique and required implicitly by USERNAME_FIELD.
    # Explicitly setting unique=True is good practice here.
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)


    # The username field is inherited from AbstractUser.
    # AbstractUser.username is max_length=150, unique=True, blank=False, null=False
    # with validators. We keep it as is, ensuring it remains required and unique.
    # No changes needed here unless you want to alter its max_length or validators,
    # but we define it below for clarity that we are keeping it.
    username = models.CharField(
        _("username"),
        max_length=150, # Default AbstractUser max_length
        unique=True,    # Default AbstractUser unique constraint
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator], # Keep default validators
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=False, # Explicitly ensure required
        null=False,  # Explicitly ensure required
    )


    # These fields are inherited from AbstractUser but default to blank=True.
    # We override them to make them required.
    first_name = models.CharField(_("first name"), max_length=150, blank=False, null=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False, null=False)


    # Set this field as the primary unique identifier for authentication.
    USERNAME_FIELD = "email"

    # These fields are required when creating a user via `createsuperuser`
    # because USERNAME_FIELD is set to email. The password is also prompted
    # automatically.
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    # Assign our custom manager to the objects attribute.
    objects = CustomUserManager()

    def __str__(self):
        """Return the email as the string representation."""
        return self.email

    # You can keep or remove other methods from AbstractUser if needed,
    # like get_full_name, get_short_name, email_user, etc.
    # Example:
    # def get_full_name(self):
    #     return f"{self.first_name} {self.last_name}".strip()
    #
    # def get_short_name(self):
    #     return self.first_name