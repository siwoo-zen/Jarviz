from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission


class UserAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("이메일은 필수입니다.")
        user = self.model(
            username=username,
            email=self.normalize_email(email),
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
    full_name = models.CharField(max_length=100)

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
        return self.username


class EmployerAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("이메일은 필수입니다.")
        employer = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        employer.set_password(password)
        employer.save(using=self._db)
        return employer

    def create_superuser(self, username, email, password=None):
        employer = self.create_user(username, email, password)
        employer.is_staff = True
        employer.is_superuser = True
        employer.save()
        return employer


class EmployerAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    company_website = models.URLField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='employeraccount_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='employeraccount_permissions',
        blank=True
    )

    objects = EmployerAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.company_name} ({self.username})"
