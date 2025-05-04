# models.py (통합 버전)
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission


class UserAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_company=False):
        if not email:
            raise ValueError("이메일은 필수입니다.")
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_company=is_company
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    full_name = models.CharField(max_length=100, blank=True, null=True)

    # 기업 계정용 필드
    is_company = models.BooleanField(default=False)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    contact_person = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='useraccount_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='useraccount_permissions',
        blank=True
    )

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{'[기업]' if self.is_company else '[사용자]'} {self.username}"
