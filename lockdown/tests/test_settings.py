from random import choice

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

SECRET_KEY = ''.join([choice('abcdefghijklmnopqrstuvwxyz'  # nosec
                             '0123456789!@#$%^&*(-_=+)')
                      for i in range(64)])

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
