# 직접 개발한 코드
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
    username = models.CharField(max_length=250, null=True)

    created_date = models.DateTimeField(auto_now_add=True, null=True)

    is_active = models.NullBooleanField(default=True, null=True)
    is_staff = models.NullBooleanField(default=False, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return '[{}]{} ( {} )'.format(self.id, self.email, self.username)

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class ApiKeyManager(models.Manager):

    def _generate_key(self):
        return sha1(str(randint(0, (16 ** 40) - 1)).encode('utf-8')).hexdigest()

    def generate(self, user):
        key = self._generate_key()

        while self.filter(key=key).count() > 0:
            key = self._generate_key()

        return self.create(user=user, key=key)

    def generate_secret(self):
        return self._generate_key()


class ApiKey(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='api_keys')
    key = models.CharField(max_length=40, null=True)
    secret_key = models.CharField(max_length=100, null=True)

    created_dt = models.DateTimeField(auto_now_add=True)

    objects = ApiKeyManager()

    def __str__(self):
        return 'id:{}, {}'.format(self.id, self.key)


class Domain(models.Model):
    api_key = models.ForeignKey(ApiKey, related_name='domains')
    domain = models.CharField(max_length=100)

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.domain)
