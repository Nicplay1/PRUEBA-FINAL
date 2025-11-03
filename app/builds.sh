#!/bin/bash
set -e

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "🔥 Build completado."
