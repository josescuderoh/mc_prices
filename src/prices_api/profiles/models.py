from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.


class UserProfileManager(BaseUserManager):
    """Helps django work with our custom user mode."""

    def create_user(self, username, name, password=None):
        """Creates a new user profile object."""

        if not username:
            raise ValueError('Users must have a username.')

        user = self.model(username=username, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, name, password):
        """Creates and saves a new superuser with the given details"""

        user = self.create_user(username, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represents a "user profile " inside our system"""

    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get user's full name."""

        return self.name

    def get_short_name(self):
        """Used to get a user's short name."""

        return self.name

    def __str__(self):
        """Django uses this when it needs to convert the object to a string"""

        return self.username
