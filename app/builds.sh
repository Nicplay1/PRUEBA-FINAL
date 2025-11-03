#!/bin/bash

# 🔹 Salir si hay un error
set -e

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Ejecutando migraciones..."
python manage.py migrate

echo "Creando usuario inicial con id_rol = 3..."

# Ejecuta un script Django para crear el usuario
python manage.py shell << END
from usuario.models import Usuario, Rol
from django.db import IntegrityError

# Intentamos obtener el rol 3
try:
    rol = Rol.objects.get(id_rol=3)
except Rol.DoesNotExist:
    rol = None
    print("⚠️ El rol con id 3 no existe. Por favor crea primero el rol.")

if rol:
    try:
        usuario, created = Usuario.objects.get_or_create(
            correo='admin@admin.com',  # Cambia este correo si quieres
            defaults={
                'nombres': 'Admin',
                'apellidos': 'Usuario',
                'tipo_documento': 'CC',
                'numero_documento': '1234567890',
                'telefono': '0000000',
                'celular': '0000000000',
                'estado': 'Activo',
                'contraseña': 'admin123',  # Aquí puedes encriptarla si quieres
                'id_rol': rol
            }
        )
        if created:
            print("✅ Usuario inicial creado correctamente.")
        else:
            print("ℹ️ El usuario ya existe.")
    except IntegrityError as e:
        print(f"❌ Error al crear el usuario: {e}")
END

echo "🔥 Build completado."
