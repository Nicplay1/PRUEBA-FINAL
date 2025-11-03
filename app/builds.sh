#!/bin/bash
set -e

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Generando migraciones..."
python manage.py makemigrations

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "🔥 Migraciones aplicadas y build completado."
