#!/usr/bin/env bash
set -o errexit

echo "🚀 Instalando dependencias..."
pip install -r requirements.txt

echo "⚙️ Limpiando base de datos..."
python manage.py migrate --fake usuario zero --noinput
python manage.py migrate --fake vigilante zero --noinput
python manage.py migrate --fake residente zero --noinput
python manage.py migrate --fake administrador zero --noinput

echo "🧩 Borrando registros antiguos de migraciones..."
python manage.py migrate --fake-initial --noinput

echo "🧱 Recreando migraciones..."
python manage.py makemigrations
python manage.py migrate --noinput

python manage.py init_datos

echo "✅ Migraciones aplicadas correctamente."
