from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from hashlib import sha1
from random import randint
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        user = self.model(email=self.normalize_email(email), is_active=True, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=self.normalize_email(email), is_staff=True, is_superuser=True, is_active=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=250, unique=True)
    username = models.CharField(max_length=20, null=True)

    created_date = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    object = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return '{} ( {} )'.format(self.email, self.username)


class ApiKeyManager(models.Manager):

    def _generate_key(self):
        return sha1(str(randint(0, (16 ** 40) - 1))).hexdigest()

    def generate(self, user):
        key = self._generate_key()

        while self.filter(key=key).count() > 0:
            key = self._generate_key()

        return self.create(user=user, key=key)


class ApiKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='api_keys')
    key = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    objects = ApiKeyManager()

    def __str__(self):
        return self.key