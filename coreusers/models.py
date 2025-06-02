from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    # افزودن related_name برای جلوگیری از تعارض‌ها
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # این نام به گروه‌ها در CustomUser اشاره می‌کند
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # این نام به مجوزها در CustomUser اشاره می‌کند
        blank=True,
    )
