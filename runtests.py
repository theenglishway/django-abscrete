#!/usr/bin/env python
import sys
import os
from os.path import abspath, dirname

import django
from django.conf import settings
from django.core.management import execute_from_command_line

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not settings.configured:
    settings.configure(
        DEBUG=False,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        },
        TEST_RUNNER="django.test.runner.DiscoverRunner",
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.messages',
            'django.contrib.sites',
            'django.contrib.admin',
            'abscrete.tests.apps.TestsConfig',
        ),
        MIDDLEWARE_CLASSES=(),
        SITE_ID=3,
        TEMPLATES=[{
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": (),
                "OPTIONS": {
                    "loaders": (
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ),
                    "context_processors": (
                        "django.template.context_processors.debug",
                        "django.template.context_processors.i18n",
                        "django.template.context_processors.media",
                        "django.template.context_processors.request",
                        "django.template.context_processors.static",
                        "django.contrib.messages.context_processors.messages",
                        "django.contrib.auth.context_processors.auth",
                    ),
                },
            },
        ],
        ROOT_URLCONF=None,
    )


DEFAULT_TEST_APPS = [
    'abscrete.tests',
]


def runtests():
    other_args = list(filter(lambda arg: arg.startswith('-'), sys.argv[1:]))
    test_apps = list(filter(lambda arg: not arg.startswith('-'), sys.argv[1:])) or DEFAULT_TEST_APPS
    argv = sys.argv[:1] + ['test', '--traceback'] + other_args + test_apps
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
