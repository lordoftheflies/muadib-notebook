"""
Django settings for muadib project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import logging
import os

from configurations import Configuration


class BaseConfiguration(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'dgeha4qla!4t$-ay43uzpuc@6ot4zpe&&@t6o2syb8$zk2(w_z'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    SITE_ID = 1

    ALLOWED_HOSTS = []

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django_extensions',

        'corsheaders',

        'rest_framework',
        'rest_framework.authtoken',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.bitbucket',
        'allauth.socialaccount.providers.github',
        'allauth.socialaccount.providers.gitlab',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.paypal',
        'allauth.socialaccount.providers.slack',
        'allauth.socialaccount.providers.windowslive',

        'rest_auth',
        'rest_auth.registration',

        'django_celery_results',
        'django_celery_beat',

        'djangobower',

        'presentation',
        'instrumentation',
        'engine',
        'simulator'

    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        'muadib.middleware.MethodOverrideMiddleware',
    ]

    ROOT_URLCONF = 'muadib.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
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

    WSGI_APPLICATION = 'muadib.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/2.0/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    REST_SESSION_LOGIN = False
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    ACCOUNT_EMAIL_REQUIRED = False
    ACCOUNT_AUTHENTICATION_METHOD = 'username'
    ACCOUNT_EMAIL_VERIFICATION = 'optional'

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            # 'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        )
    }

    # Password validation
    # https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    AUTHENTICATION_BACKENDS = (
        # Needed to login by username in Django admin, regardless of `allauth`
        'django.contrib.auth.backends.ModelBackend',

        # `allauth` specific authentication methods, such as login by e-mail
        'allauth.account.auth_backends.AuthenticationBackend',
    )

    CELERY_RESULT_BACKEND = 'django-db'

    # Internationalization
    # https://docs.djangoproject.com/en/2.0/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')
    BOWER_INSTALLED_APPS = (
        "PolymerElements/app-layout#^2.0.0",
        "PolymerElements/app-route#^2.0.0",
        "PolymerElements/iron-ajax#^2.1.3",
        "PolymerElements/iron-flex-layout#^2.0.0",
        "PolymerElements/iron-iconset-svg#^2.0.0",
        "PolymerElements/iron-icon",
        "PolymerElements/iron-image#^2.2.0",
        "PolymerElements/iron-input#^2.1.1",
        "PolymerElements/iron-list#^2.0.14",
        "PolymerElements/iron-media-query#^2.0.0",
        "PolymerElements/iron-pages#^2.0.0",
        "PolymerElements/iron-selector#^2.0.0",
        "PolymerElements/paper-button",
        "PolymerElements/paper-card#^2.1.0",
        "PolymerElements/paper-checkbox#^2.0.2",
        "PolymerElements/paper-dialog#^2.1.1",
        "PolymerElements/paper-dropdown-menu#^2.0.3",
        "PolymerElements/paper-fab#^2.1.0",
        "PolymerElements/paper-icon-button#^2.0.0",
        "PolymerElements/paper-input#^2.2.0",
        "PolymerElements/paper-item#^2.1.1",
        "PolymerElements/paper-listbox#^2.1.0",
        "PolymerElements/paper-menu-button#^2.1.0",
        "PolymerElements/paper-progress#^2.1.0",
        "PolymerElements/paper-radio-button#^2.0.0",
        "PolymerElements/paper-radio-group#^2.1.0",
        "PolymerElements/paper-spinner#^2.1.0",
        "PolymerElements/paper-tabs#^2.0.0",
        "PolymerElements/paper-toast#^2.1.0",
        "Polymer/polymer#^2.0.0",
        "webcomponents/webcomponentsjs#^1.0.0",
        "web-animations-js#^2.3.1",
        "socket.io-client#^2.0.1",
        "chartjs#2.7.1",
        "chartjs-plugin-datalabels#0.2.0",
        "git://github.com/lordoftheflies/moment-js#^0.7.2",
        "git://github.com/lordoftheflies/paper-time-picker#master",
    )

    # Add it on your settings.py file
    # STATICFILES_DIRS = [
    #     os.path.join(BASE_DIR, "static"),  # your static/ files folder
    # ]
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'djangobower.finders.BowerFinder',
        #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'console.log',
                'formatter': 'verbose'
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            # 'django': {
            #     'handlers': ['file'],
            #     'level': 'DEBUG',
            #     'propagate': True,
            # },
            # 'django.request': {
            #     'handlers': ['mail_admins'],
            #     'level': 'ERROR',
            #     'propagate': False,
            # },
            'muadib': {
                'handlers': ['console'],
                'level': 'DEBUG'
            }
        },
    }

    SOCKETIO_PORT = 9001
    SOCKETIO_HOST = ''
    # SOCKETIO_ASYNC_MODE = 'gevent'
    # SOCKETIO_ASYNC_MODE = 'gevent_uwsgi'
    SOCKETIO_ASYNC_MODE = 'threading'

    VISA_LIBRARY = '%s@sim' % os.path.join(BASE_DIR, 'instrumentation.yaml')


class DevelopmentConfiguration(BaseConfiguration):
    """
    Configuration for development.
    """
    DEBUG = True

    @classmethod
    def pre_setup(cls):
        super(DevelopmentConfiguration, cls).pre_setup()
        logging.info('Setup configuration: %s ...', cls)

    @classmethod
    def setup(cls):
        super(DevelopmentConfiguration, cls).setup()
        logging.info('Configuration settings loaded: %s', cls)

    @classmethod
    def post_setup(cls):
        super(DevelopmentConfiguration, cls).post_setup()
        logging.debug("Configuration setup succeed: %s", cls)


class StagingConfiguration(BaseConfiguration):
    """
    Configuration for staging.
    """
    DEBUG = True

    @classmethod
    def pre_setup(cls):
        super(StagingConfiguration, cls).pre_setup()
        logging.info('Setup configuration: %s ...', cls)

    @classmethod
    def setup(cls):
        super(StagingConfiguration, cls).setup()
        logging.info('Configuration settings loaded: %s', cls)

    @classmethod
    def post_setup(cls):
        super(StagingConfiguration, cls).post_setup()
        logging.debug("Configuration setup succeed: %s", cls)


class ProductionConfiguration(BaseConfiguration):
    """
    Configuration for production.
    """
    DEBUG = False

    @classmethod
    def pre_setup(cls):
        super(ProductionConfiguration, cls).pre_setup()
        logging.info('Setup configuration: %s ...', cls)

    @classmethod
    def setup(cls):
        super(ProductionConfiguration, cls).setup()
        logging.info('Configuration settings loaded: %s', cls)

    @classmethod
    def post_setup(cls):
        super(ProductionConfiguration, cls).post_setup()
        logging.debug("Configuration setup succeed: %s", cls)
