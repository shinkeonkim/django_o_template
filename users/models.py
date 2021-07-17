from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
  def create_user(self, email, password, nickname=""):
    if not email:
      raise ValueError(_('Users must have an email address'))
    
    user = self.model(
      email = self.normalize_email(email),
      nickname = nickname,
    )
    user.set_password(password)
    user.save()

    return user 

  def create_superuser(self, email, password):
    user = self.create_user(
      email=email,
      password=password,
    )

    user.is_superuser = True
    user.is_active = True
    user.save()

    return user


class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(
    verbose_name=_('Email address'),
    max_length=255,
    unique=True,
  )
  nickname = models.CharField(
    verbose_name=_("Nickname"),
    max_length=255,
    null=True,
    blank=True,
  )
  first_name = models.CharField(
    verbose_name=_("First name"),
    max_length=255,
    null=True,
    blank=True,
  )
  last_name = models.CharField(
    verbose_name=_("Last name"),
    max_length=255,
    null=True,
    blank=True,
  )
  phone = models.CharField(
    max_length=100,
    null=True,
    blank=True,
  )
  is_active = models.BooleanField(
    verbose_name=_("Is active"),
    default=False,
  )
  created_at = models.DateTimeField(
    verbose_name=_('created_at'),
    auto_now_add=True,
  )
  updated_at = models.DateTimeField(
    verbose_name=_('updated_at'),
    auto_now=True,
  )

  objects = UserManager()

  USERNAME_FIELD = 'email'

  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')
    ordering = ('-created_at',)
  
  def __str__(self) -> str:
    return self.email
  
  @property
  def full_name(self) -> str:
    return "".join([self.first_name or '', ' ' if self.last_name else '', self.last_name or ''])

  @property
  def is_staff(self):
    return self.is_superuser
