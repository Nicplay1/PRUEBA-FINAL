#!/usr/bin/env bash
set -o errexit

echo "🚀 Instalando dependencias..."
pip install -r requirements.txt

echo "⚙️ Limpiando base de datos..."
# Deshacer migraciones de tus apps
python manage.py migrate --fake usuario zero --noinput
python manage.py migrate --fake vigilante zero --noinput
python manage.py migrate --fake residente zero --noinput
python manage.py migrate --fake administrador zero --noinput

echo "🧹 Eliminando todos los datos existentes..."
python manage.py flush --no-input

echo "🧩 Aplicando migraciones existentes..."
python manage.py migrate --fake-initial --noinput
python manage.py migrate --noinput

python manage.py collectstatic --noinput

python manage.py init_datos

echo "✅ Migraciones aplicadas y base de datos limpia."
