from pathlib import Path
import os
import dj_database_url # データベース用（もし使う場合）
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- 1. セキュリティ設定 ---
# Renderの環境変数から取得、なければ開発用キーを使う
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-dev')

# Render上ではFalse、手元ではTrueにする（環境変数で制御）
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Renderのドメインとローカルを許可
ALLOWED_HOSTS = ['*'] # 本来は ['.onrender.com', 'localhost', '127.0.0.1'] が理想


# --- 2. アプリ定義 ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "testApp",
    "shop",
    "whitenoise.runserver_nostatic", # CSS用に追加
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # CSS用（必ずSecurityMiddlewareの下）
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
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

WSGI_APPLICATION = "core.wsgi.application"

# --- 3. データベース設定 (SQLiteを使用) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- 4. パスワードバリデーション ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- 5. 言語・時刻設定 ---
LANGUAGE_CODE = "ja" # 日本語に変更
TIME_ZONE = "Asia/Tokyo" # 日本時間に変更
USE_I18N = True
USE_TZ = True

# --- 6. 静的ファイル (CSS/JavaScript) 設定 ---
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise が静的ファイルを効率的に配信するための設定
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- 7. ログイン・リダイレクト設定 ---
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'timeline'
LOGOUT_REDIRECT_URL = 'timeline'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"