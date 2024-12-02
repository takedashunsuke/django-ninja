from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'debug_toolbar',
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

ACCOUNT_EMAIL_VERIFICATION = 'none'  # メール認証なし

FRONTEND_URL = "https://mysite-eesq.onrender.com"