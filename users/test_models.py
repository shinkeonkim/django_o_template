from django.test import TestCase
from .models import User
from django.utils.translation import ugettext_lazy as _
from config.settings import INSTALLED_APPS, AUTH_USER_MODEL

class SettingsAboutUsersAppTest(TestCase):    
    def test_account_is_configured(self):
        self.assertTrue('users' in INSTALLED_APPS)
        self.assertTrue('users.User' == AUTH_USER_MODEL)


class UserModelFieldTest(TestCase):
  def setUp(self):
    self.user = User.objects.create(
      email='test@test.com',
      password='password',
      nickname=''
    )

  def test_is_active_field_default_value(self):
    self.assertFalse(self.user.is_active)

  def test_user_model_has_is_active_field(self):
    self.user.save()
    self.assertIsInstance(self.user.is_active, bool)

class SuperUserTest(TestCase):
  def setUp(self):
    self.user = User.objects.create_superuser(
      email='admin@test.com',
      password='password'
    )
    self.user.is_superuser = True
    self.user.save()

  def test_super_user_login(self):
    self.assertIsInstance(self.user, User)
    self.assertTrue(self.client.login(email='admin@test.com', password='password'))

  def test_super_user_default_active(self):
    self.assertTrue(self.user.is_active)


class UserTest(TestCase):
  def setUp(self):
    self.active_user = User.objects.create_user(
      email='test@test.com',
      password='password',
      nickname=''
    )
    self.active_user.is_active = True
    self.active_user.save()

    self.inactive_user = User.objects.create_user(
      email='test2@test.com',
      password='password',
      nickname=''
    )

  def test_user_login(self):
    self.assertIsInstance(self.active_user, User)
    self.assertTrue(self.client.login(email='test@test.com', password='password'))

  def test_inactive_user_can_not_login(self):
    self.assertIsInstance(self.inactive_user, User)
    self.assertFalse(self.client.login(email='test2@test.com', password='password'))

  def test_user_email_required_value(self):
    with self.assertRaises(TypeError):
      User.objects.create_user(
        nickname='koa',
        password='password',
      )
    with self.assertRaises(ValueError):
      User.objects.create_user(
        email='',
        nickname='koa',
        password='password',
      )
    

class UserModelPropertyTest(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(
      email='test@test.com',
      password='password',
    )
  
  def test_full_name(self):
    self.assertTrue(hasattr(self.user, 'full_name'))
    self.assertIsInstance(self.user.full_name, str)
    with self.assertRaises(Exception):
      self.user.full_name = 'koa kim'
    self.assertEqual(self.user.full_name, '')
    self.user.first_name = 'koa'
    self.user.save()
    self.assertEqual(self.user.full_name, 'koa')
    self.user.last_name = 'kim'
    self.user.save()
    self.assertEqual(self.user.full_name, 'koa kim')
  
  def test_is_staff(self):
    self.assertFalse(self.user.is_staff)
    self.user.is_superuser = True
    self.user.save()
    self.assertTrue(self.user.is_staff)

  def test_username_field(self):
    self.assertEqual(self.user.USERNAME_FIELD, 'email')
    self.assertIsInstance(self.user.USERNAME_FIELD, str)

  def test_stringify_user_model(self):
    self.assertEqual(str(self.user), 'test@test.com')
