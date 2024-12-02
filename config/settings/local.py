from .base import *

DEBUG = True
ALLOWED_HOSTS=['*']

# SQLite 設定を引き継ぐ
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

ACCOUNT_EMAIL_VERIFICATION = 'none'  # メール認証なし
print("local.py settings are loaded.")