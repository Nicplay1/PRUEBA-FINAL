#!/usr/bin/env bash
#set -o errexit

#echo "🚀 Instalando dependencias..."
#ip install -r requirements.txt

#echo "⚙️ Limpiando base de datos..."
# Deshacer todas las migraciones de tus apps
#python manage.py migrate usuario zero --noinput || true
#ython manage.py migrate vigilante zero --noinput || true
#python manage.py migrate residente zero --noinput || true
#python manage.py migrate administrador zero --noinput || true

# Deshacer migraciones de apps Django internas para forzar recreación
#python manage.py migrate admin zero --noinput || true
#python manage.py migrate auth zero --noinput || true
#python manage.py migrate contenttypes zero --noinput || true
#python manage.py migrate sessions zero --noinput || true

#echo "🧹 Eliminando todos los datos existentes..."
#python manage.py flush --no-input || true

#echo "🧩 Aplicando migraciones desde cero..."
# Aplica todas las migraciones sin --fake para crear columnas nuevas
#python manage.py migrate --noinput

#echo "📦 Creando datos iniciales..."
#python manage.py init_datos

#echo "✅ Migraciones aplicadas y base de datos limpia."



#!/usr/bin/env bash
set -o errexit

echo "🚀 Instalando dependencias..."
pip install -r requirements.txt

echo "⚙️ Aplicando migraciones nuevas..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "📦 Cargando datos iniciales si faltan..."
python manage.py init_datos || true

echo "✅ Base de datos actualizada sin eliminar datos."
