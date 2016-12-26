from random import choice

from pkg_resources import parse_version

import django

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

SECRET_KEY = ''.join([choice('abcdefghijklmnopqrstuvwxyz'
                             '0123456789!@#$%^&*(-_=+)')
                      for i in range(64)])

# Handle differences in the configuration of old- and new-style middlewares.
if parse_version(django.get_version()) < parse_version('1.10'):
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware'
    )
else:
    MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware'
    ]

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'lockdown'
)

ROOT_URLCONF = 'lockdown.tests.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
