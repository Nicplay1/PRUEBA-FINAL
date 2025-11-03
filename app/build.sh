#!/bin/bash
set -e

echo "🚀 Instalando dependencias..."
pip install -r requirements.txt

echo "⚙️ Aplicando migraciones..."
python manage.py makemigrations usuario vigilante residente administrador
python manage.py showmigrations usuario
python manage.py migrate --noinput

echo "✅ Migraciones aplicadas correctamente."
