from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group
from django.db import models

# Create your models here.
from django.db.models import EmailField, CharField, BooleanField, DateTimeField


class MyAccountManager(BaseUserManager):
    def create_user(self, email, fullname, password=None):
        if not email:
            raise ValueError('User must provide email.')

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        if not user.is_instructor:
            instructor_group = Group.objects.get(name='students')
            user.groups.add(instructor_group)

    def create_superuser(self, email, fullname, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            fullname=fullname,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email = EmailField(verbose_name='email', max_length=60, unique=True)
    fullname = CharField(max_length=30, unique=True)
    is_instructor = BooleanField(default=False)
    date_join = DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = DateTimeField(verbose_name='last login', auto_now_add=True)
    is_admin = BooleanField(default=False)
    is_active = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
