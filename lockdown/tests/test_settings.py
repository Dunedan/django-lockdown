from random import choice

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

SECRET_KEY = ''.join([choice('abcdefghijklmnopqrstuvwxyz'
                             '0123456789!@#$%^&*(-_=+)')
                      for i in range(64)])

MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware'
                      )

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'lockdown'
)

ROOT_URLCONF = 'lockdown.tests.urls'
