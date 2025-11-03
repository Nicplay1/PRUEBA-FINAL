#!/bin/bash
set -e

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Aplicando migraciones..."
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput || true

echo "Build completado ✅"
