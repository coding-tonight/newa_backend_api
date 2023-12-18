from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class AuthUserManager(BaseUserManager):
    """ create custom user manager for custom user model
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_('Email Field is required.'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
      Create and save a SuperUser with the given email and password.
      """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('User must be staff or is_staff must be True'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('User must be superuser or super must be True'))

        return self.create_user(email, password, **extra_fields)
