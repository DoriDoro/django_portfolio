"""
Django Local Settings Template

By importing from `oc_lettings_site.settings import *`, this template inherits all the
configurations defined in the main settings.py file. This ensures that all the default settings
and configurations are preserved, providing a solid foundation for the locale development
environment.
"""

from portfolio.settings import *  # noqa

"""
The SECRET_KEY is a cryptographic key used by Django to provide cryptographic signing, and should
be kept secret. You can generate a random key using the following command:
$ python manage.py shell -c 'from django.core.management import utils;
print(utils.get_random_secret_key())'
"""
SECRET_KEY = "YOUR_GENERATED_SECRET_KEY_HERE"

"""
The `DEBUG = True` setting enables debug mode, which is essential for development.Debug mode
provides detailed error pages and additional debugging information, making it easier to diagnose
and fix issues during development.
"""
DEBUG = True

"""
The ALLOWED_HOSTS setting is configured to include 'localhost' and '127.0.0.1', allowing the
Django application to serve requests from the locale machine.This is a common configuration
for development environments, ensuring that the application can be accessed locally.
"""
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

"""
The template includes placeholders for Sentry DSN(SENTRY_DSN=).Sentry is a popular error tracking
tool that helps developers monitor and fix crashes in real-time.By configuring Sentry in the
locale settings, developers can easily track errors and exceptions that occur during development,
improving the overall quality and stability of the application.
https://docs.sentry.io/platforms/python/integrations/django/#install
"""
# SENTRY_DSN =
