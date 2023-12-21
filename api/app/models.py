import uuid

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from app.managers import AuthUserManager

# Create your models here.


class AuthUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=45, null=True)
    last_name = models.CharField(max_length=45, null=True)
    profile = models.ImageField(upload_to='uploads/usr/profile/', null=True)
    phone_number = models.CharField(max_length=14, null=True)
    distrist = models.CharField(max_length=45, null=True)
    city = models.CharField(max_length=45, null=True)
    province = models.CharField(max_length=45, null=True)
    is_verify = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AuthUserManager()

    class Meta:
        db_table = 'auth_user'

    def __str__(self) -> str:
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

# generate uuid


def generate_uuid():
    return uuid.uuid4().hex


class Base(models.Model):
    uuid = models.UUIDField(default=generate_uuid(), editable=False)
    created_at = models.DateTimeField(auto_now=False, null=True)
    created_by = models.ForeignKey(
        AuthUser, related_name="+", on_delete=models.PROTECT, null=True)
    updated_at = models.DateTimeField(auto_now=False)
    updated_by = models.ForeignKey(
        AuthUser, related_name="+", on_delete=models.PROTECT)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True

    #  to prevent duplicate uuid
    #  below method override default save method and also check duplicate uuid
    def save(self, *args, **kwargs):
        if not self.pk:
            while True:
                if not self.__class__.objects.filter(uuid=self.uuid).exists():
                    break

                self.uuid = uuid.uuid4().hex
        super().save(*args, **kwargs)


# otp models
class Otp(models.Model):
    user = models.ForeignKey(AuthUser, related_name="+",
                             on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)

    class Meta:
        db_table = 'otp'
