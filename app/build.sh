#!/usr/bin/env bash
set -o errexit

echo "🚀 Instalando dependencias..."
pip install -r requirements.txt

echo "⚙️ Limpiando base de datos..."
# Deshacer migraciones fake de tus apps
python manage.py migrate --fake usuario zero --noinput
python manage.py migrate --fake vigilante zero --noinput
python manage.py migrate --fake residente zero --noinput
python manage.py migrate --fake administrador zero --noinput

echo "🧹 Eliminando todos los datos existentes..."
python manage.py flush --no-input

echo "🧩 Aplicando migraciones existentes..."
# Aplica migraciones reales ahora, no solo fake
python manage.py makemigrations
python manage.py migrate --fake-initial --noinput

echo "🗂️ Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "⚡ Inicializando datos..."
python manage.py init_datos

echo "✅ Migraciones aplicadas y base de datos limpia."
