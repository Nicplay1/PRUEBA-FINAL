#!/bin/bash
set -e

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Aplicando migraciones..."
cd app
python manage.py makemigrations
python manage.py migrate --noinput

echo "🔥 Migraciones aplicadas correctamente."
