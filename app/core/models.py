from django.db import models
from django.conf import settings

# Create your models here.
"""creating the user models"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extrafields):
        if not email :
            raise ValueError('email missing')
        user = self.model(email=self.normalize_email(email),**extrafields)

        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_superuser(self, email, password):

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user






class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    time_minute =models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

class Tag(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name