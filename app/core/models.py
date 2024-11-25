from django.db import models

# Create your models here.
"""creating the user models"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extrafields):

        user = self.model(email=self.normalize_email(email),**extrafields)

        user.set_password(password)
        user.save(using=self._db)

        return user








class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'