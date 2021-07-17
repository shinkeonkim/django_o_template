from django.test import TestCase
from config import settings
import mock

class DatabaseSettingsTest(TestCase):
  @mock.patch('config.settings.USE_DOCKER', True)
  @mock.patch('config.settings.DATABASES', {
    "default": {
      "ENGINE": "django.db.backends.postgresql",
      "HOST": "db",
    }
  })
  def test_when_use_docker_database_is_postgres(self):
    self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.postgresql')
