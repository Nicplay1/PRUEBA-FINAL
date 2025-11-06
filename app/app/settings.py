"""
Django settings for app project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-pf7lx3f(rk7&qqs33&(#sfgg2-_d=g9f9g=bfw2e5gr59vhnrt'
DEBUG = True

ALLOWED_HOSTS = ['prueba-final-6586.onrender.com', 'localhost', '127.0.0.1']

# ---------------------------------------
# 🧩 APLICACIONES
# ---------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'usuario',
    'administrador',
    'residente',
    'vigilante',
    'crispy_forms',
    'channels',
]

# ---------------------------------------
# ⚙️ MIDDLEWARE (se agregó Whitenoise)
# ---------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Debe ir justo aquí
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middlewares.NoCacheMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Channels
ASGI_APPLICATION = "app.asgi.application"

# Configurar Redis para producción
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# ---------------------------------------
# 🗄️ BASE DE DATOS (Render PostgreSQL)
# ---------------------------------------
import pymysql
pymysql.install_as_MySQLdb()

# Opción: cambiar 'default_db' a 'mysql' o 'postgres' según la base que quieras usar
default_db = 'postgres'  # 'mysql' o 'postgres'

if default_db == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'proyecto_bd',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }
elif default_db == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'proyecto_bd_c4on',
            'USER': 'proyecto_bd_c4on_user',
            'PASSWORD': 'eV16YhehCwxaSkIWw8MpEHmmNvVtKC8G',
            'HOST': 'dpg-d43t4rili9vc73dfutn0-a.oregon-postgres.render.com',
            'PORT': '5432',
            'OPTIONS': {
                'sslmode': 'require'
            }
        }
    }
# ---------------------------------------
# 🔐 VALIDACIÓN DE CONTRASEÑAS
# ---------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------
# 🌎 INTERNACIONALIZACIÓN
# ---------------------------------------
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# ---------------------------------------
# 🎨 ARCHIVOS ESTÁTICOS Y MULTIMEDIA
# ---------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ✅ requerido por Render

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ✅ Whitenoise (sirve estáticos comprimidos en Render)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------
# 📧 CONFIGURACIÓN DE CORREO
# ---------------------------------------
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

# Tu API Key de SendGrid (desde variables de entorno)
SENDGRID_API_KEY = os.getenv("EMAIL_HOST_PASSWORD")

# Opciones de depuración (opcional)
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_ECHO_TO_STDOUT = True

# Correo por defecto
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "altosdefontibon.cr@gmail.com")


# 🟢 En Render, solo mostrar el correo en consola (no enviarlo)

# ---------------------------------------
# 🧱 CONFIG EXTRA
# ---------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
