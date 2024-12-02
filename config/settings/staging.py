from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'debug_toolbar',
]

# SQLite の設定
default_dburl = "sqlite:///" + str(os.path.join(BASE_DIR) / "db.sqlite3")

# 本場環境では、DATABASE_URLにPostgreSQLのURLを指定する
DATABASES = {
    "default": config("DATABASE_URL", default=default_dburl, cast=dburl),
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

ACCOUNT_EMAIL_VERIFICATION = 'none'  # メール認証なし

FRONTEND_URL = "https://mysite-eesq.onrender.com"