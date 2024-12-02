from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'debug_toolbar',
]

ACCOUNT_EMAIL_VERIFICATION = 'none'  # メール認証なし

FRONTEND_URL = "https://mysite-eesq.onrender.com"