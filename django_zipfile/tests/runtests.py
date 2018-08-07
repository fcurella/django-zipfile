#!/usr/bin/env python
import sys
from os import path
from django.conf import settings

PROJECT_DIR = path.dirname(path.realpath(__file__))


settings.configure(
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3'}
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django_zipfile'
    ],
    ROOT_URLCONF='django_zipfiles.tests.urls',
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'DIRS': [
                path.join(PROJECT_DIR, 'templates'),
            ],
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ),
    ALLOWED_HOSTS=['*'],
    SITE_ID=1,
)


def runtests(*test_args):
    import django.test.utils
    django.setup()
    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['django_zipfile'])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
