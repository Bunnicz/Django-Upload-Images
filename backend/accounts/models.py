import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username: str, password: str, *args, **kwargs):
        """Custom User creation"""
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(username=username, *args, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username: str, password: str, *args, **kwargs):
        """Custom SuperUser creation"""
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(username=username, password=password, *args, **kwargs)


class UserTier(models.Model):
    """User tier model"""

    class Meta:
        db_table = "Tiers"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.name}"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    img_px200 = models.BooleanField(default=True)
    img_px400 = models.BooleanField(default=False)
    img_native = models.BooleanField(default=False)
    generated_url = models.BooleanField(default=False)


class CustomUser(AbstractUser):
    """Custom user model"""

    class Meta:
        db_table = "Users"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.username}-{self.tier}"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    tier = models.ForeignKey(
        UserTier,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
