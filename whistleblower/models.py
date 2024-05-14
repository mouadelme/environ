from botocore.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    allowed_extensions = ('pdf', 'txt', 'jpg')
    file_extension = value.name.lower().split('.')[-1]
    if not file_extension in allowed_extensions:
        allowed_extensions_formatted = ", ".join(allowed_extensions)
        raise ValidationError(f"Unsupported file type. Allowed file types are: {allowed_extensions_formatted}")


class UploadFile(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('IP', 'In Progress'),
        ('R', 'Resolved'),
    ]

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    picture = models.FileField(null=True, blank=True, validators=[validate_file_extension])
    username = models.CharField(max_length=50, default='', blank=True)
    email = models.CharField(max_length=50, default='', blank=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='New')
    reason = models.TextField(max_length=300, default='', blank=True)
    company = models.CharField(max_length=50, default='', blank=True)

    explanation = models.TextField(max_length=300, default='', blank=True)
    public = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)


class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='whistleblower_users_groups')
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='whistleblower_user_permissions'
    )
    is_user = models.BooleanField('user status', default=True)
    is_admin = models.BooleanField('site admin status', default=False)


def is_admin_group(user):
    return user.groups.filter(name='Admin').exists()
