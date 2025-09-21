from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    Group,
    PermissionsMixin,
    Permission,
)


class CustomUserManager(BaseUserManager):
    def create_student(
        self,
        last_name=None,
        first_name=None,
        user_name=None,
        user_type="student",
        password=None,
    ):
        if not all([last_name, first_name, user_name, password]):
            raise ValueError("all fields are required")

        if CustomUser.objects.filter(user_name=user_name).exists():
            raise ValueError("user_name is aleady exist.")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            user_name=user_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_teacher(
        self,
        user_type="teacher",
        first_name=None,
        last_name=None,
        user_name=None,
        password=None,
    ):
        if not all(
            user_type="teacher",
            first_name=None,
            last_name=None,
            user_name=None,
            password=None,
        ):
            raise ValueError("all fields are required")

        if CustomUser.objects.filter(user_name=user_name).exists():
            raise ValueError("user_name is already exist")

        user = self.model(
            first_name=first_name,
            user_type=user_type,
            last_name=last_name,
            user_name=user_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(
        self,
        user_type="admin",
        first_name=None,
        last_name=None,
        user_name=None,
        password=None,
    ):

        if not all([first_name, last_name, user_name, password]):
            raise ValueError("all fields are required")

        if CustomUser.objects.filter(user_name=user_name).exists():
            raise ValueError("user_name is already exist")

        user = self.model(
            first_name=first_name,
            user_type=user_type,
            last_name=last_name,
            user_name=user_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    USER_TYPES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
    ]

    first_name = models.CharField(null=False, blank=False, max_length=100)
    last_name = models.CharField(null=False, blank=False, max_length=100)
    user_name = models.CharField(null=False, blank=False, max_length=100, unique=True)
    user_type = models.CharField(
        choices=USER_TYPES, default="student", blank=False, null=False
    )
    # active_mode = models.BooleanField(null=False, blank=False, default=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="customuser_set",
        related_query_name="customuser",
    )

    objects = CustomUserManager()
    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.user_name}"
