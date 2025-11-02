#!/usr/bin/env bash
# build.sh - Script de despliegue para Render o servidores similares

# 🔹 Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# 🔹 Ejecutar migraciones
echo "Aplicando migraciones..."
python manage.py migrate

# 🔹 Crear usuario base (solo si no existe)
echo "Creando usuario inicial..."
python manage.py shell <<EOF
from app.models import Usuario, Rol
from django.db import IntegrityError

try:
    # Verifica si existe el rol con id 3
    rol = Rol.objects.filter(id_rol=3).first()
    if not rol:
        rol = Rol.objects.create(id_rol=3, nombre_rol='Usuario Base')

    # Crea un usuario solo si no existe ese correo
    if not Usuario.objects.filter(correo='admin@render.com').exists():
        Usuario.objects.create(
            nombres='Admin',
            apellidos='Render',
            tipo_documento='CC',
            numero_documento='123456789',
            correo='admin@render.com',
            telefono='0000000',
            celular='0000000000',
            contraseña='admin123',
            id_rol=rol
        )
        print("✅ Usuario creado con éxito.")
    else:
        print("ℹ️ El usuario ya existe, no se creó uno nuevo.")

except IntegrityError as e:
    print(f"⚠️ Error de integridad: {e}")
except Exception as e:
    print(f"⚠️ Error general: {e}")
EOF
