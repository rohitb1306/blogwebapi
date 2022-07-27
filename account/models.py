from autoslug import AutoSlugField
from django.db import models  # noqa
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone


# Create your models here.
class customAccountManager(BaseUserManager):
    def create_user(
        self, user_email, user_name, first_name, password, last_name="", **otherfields
    ):
        if not user_email:
            raise ValueError("provide email address")

        email = self.normalize_email(user_email)
        user = self.model(
            user_email=user_email,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            **otherfields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, user_email, first_name, user_name, password, **other_fields
    ):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True."
            )
        return self.create_user(
            user_email, user_name, first_name, password, **other_fields
        )


class MyUser(AbstractBaseUser, PermissionsMixin):
    user_email = models.EmailField(unique=True)
    user_contact = models.BigIntegerField(null=True, default=00000)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    user_name = models.CharField(max_length=30, unique=True)
    is_auther = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    new_slug = AutoSlugField(populate_from='user_name',
                             null=True, default=None)

    user_image = models.ImageField(
        upload_to="media/account/images", default="")
    sign_up_date = models.DateTimeField(default=timezone.now)

    objects = customAccountManager()

    USERNAME_FIELD = "user_email"
    REQUIRED_FIELDS = ["user_name", "first_name"]

    def __str__(self):
        return self.user_name
