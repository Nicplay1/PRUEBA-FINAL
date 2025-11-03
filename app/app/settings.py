"""
Django settings for app project.
"""

from pathlib import Path
import os
import dj_database_url  # ✅ importante para manejar la DB de Render correctamente

# ---------------------------------------
# 📂 RUTAS BASE
# ---------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------
# 🔑 SEGURIDAD
# ---------------------------------------
SECRET_KEY = 'django-insecure-pf7lx3f(rk7&qqs33&(#sfgg2-_d=g9f9g=bfw2e5gr59vhnrt'
DEBUG = True  # Cambia a False si quieres ocultar errores en producción

ALLOWED_HOSTS = [
    'prueba-final-6586.onrender.com',
    'localhost',
    '127.0.0.1'
]

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
    'usuario',
    'administrador',
    'residente',
    'vigilante',
    'crispy_forms',
    'crispy_bootstrap5',
]

# ---------------------------------------
# ⚙️ MIDDLEWARE
# ---------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Sirve archivos estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middlewares.NoCacheMiddleware',
]

ROOT_URLCONF = 'app.urls'

# ---------------------------------------
# 🎨 TEMPLATES
# ---------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # ✅ ruta correcta
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

WSGI_APPLICATION = 'app.wsgi.application'

# ---------------------------------------
# 🗄️ BASE DE DATOS (PostgreSQL Render)
# ---------------------------------------
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
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  # Carpeta con tus archivos CSS, JS, IMG
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Donde Django los recopila

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ✅ Whitenoise: sirve estáticos comprimidos
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------
# 📧 CORREO (Gmail)
# ---------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'altosdefontibon.cr@gmail.com'
EMAIL_HOST_PASSWORD = 'heho zywq sayt pexm'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# 🟢 En Render, usar consola para correos (no enviar realmente)
if os.environ.get("RENDER"):
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEBUG = False  # ✅ importante para que carguen los archivos estáticos en producción

# ---------------------------------------
# 🧱 CONFIG EXTRA
# ---------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'
