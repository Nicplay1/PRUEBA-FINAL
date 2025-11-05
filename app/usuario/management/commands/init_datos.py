from django.core.management.base import BaseCommand
from usuario.models import Rol, ZonaComun, TipoArchivo, Parqueadero, Usuario

class Command(BaseCommand):
    help = "Inserta datos iniciales en las tablas rol, zona_comun, tipo_archivo, parqueadero y usuario admin"

    def handle(self, *args, **options):
        # ------------------ ROL ------------------
        roles = [
            'Usuario',
            'Residente',
            'Admin',
            'Vigilante',
        ]
        for nombre in roles:
            obj, created = Rol.objects.get_or_create(nombre_rol=nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Rol '{nombre}' creado"))
            else:
                self.stdout.write(f"⚠️ Rol '{nombre}' ya existía")

        # ------------------ ZONA COMUN ------------------
        zonas = [
            ('Gimnasio', 50, 'Evento', 30000.00),
            ('Zona yoga', 30, 'Por hora', 30000.00),
            ('Salón de juegos', 40, 'Franja horaria', 2000.00),
            ('Lavandería', 10, 'Franja horaria', 4000.00),
            ('Zona crearte', 10, 'Evento', 100000.00),
            ('Salón social premium', 15, 'Evento', 250000.00),
            ('Salón social', 40, 'Evento', 150000.00),
            ('Oratorio', 40, 'Franja horaria', 1000.00),
            ('Salón infantil', 25, 'Franja horaria', 1000.00),
            ('Zona juegos infantil', 20, 'Franja horaria', 0.00),
            ('Cancha libre', 30, 'Por hora', 10000.00),
            ('Zona bbq 1', 8, 'Evento', 50000.00),
            ('Zona bbq 2', 8, 'Evento', 50000.00),
            ('Zonas verdes', 0, 'Franja horaria', 0.00),
        ]
        for nombre, capacidad, tipo, tarifa in zonas:
            obj, created = ZonaComun.objects.get_or_create(
                nombre_zona=nombre,
                defaults={
                    "capacidad": capacidad,
                    "tipo_pago": tipo,
                    "tarifa_base": tarifa,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Zona común '{nombre}' creada"))
            else:
                self.stdout.write(f"⚠️ Zona común '{nombre}' ya existía")

        # ------------------ TIPO ARCHIVO ------------------
        tipos_archivo = ['SOAT', 'Tarjeta de propiedad', 'Técnico-mecánica', 'Licencia', 'Identidad']
        for tipo in tipos_archivo:
            obj, created = TipoArchivo.objects.get_or_create(tipo_documento=tipo)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Tipo archivo '{tipo}' creado"))
            else:
                self.stdout.write(f"⚠️ Tipo archivo '{tipo}' ya existía")

        # ------------------ PARQUEADERO ------------------
        parqueaderos = [
            (1, 'A001', False, True),
            (2, 'A002', True, False),
            (3, 'A003', False, True),
            (4, 'A004', True, True),
            (5, 'B001', False, False),
            (6, 'B002', True, True),
            (7, 'B003', False, True),
            (8, 'B004', True, False),
            (9, 'C001', False, True),
            (10, 'C002', True, True),
            (11, 'C003', False, False),
            (12, 'C004', True, True),
            (13, 'D001', False, True),
            (14, 'D002', True, False),
            (15, 'D003', False, True),
            (16, 'D004', True, True),
            (17, 'E001', False, False),
            (18, 'E002', True, True),
            (19, 'E003', False, True),
            (20, 'E004', True, False),
        ]
        for id_p, num, comunal, estado in parqueaderos:
            obj, created = Parqueadero.objects.get_or_create(
                id_parqueadero=id_p,
                defaults={
                    "numero_parqueadero": num,
                    "comunal": comunal,
                    "estado": estado,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Parqueadero '{num}' creado"))
            else:
                self.stdout.write(f"⚠️ Parqueadero '{num}' ya existía")

        # ------------------ USUARIO ADMIN ------------------
        rol_admin = Rol.objects.get(id_rol=3)  # Admin
        admin_usuario, created = Usuario.objects.get_or_create(
            numero_documento="admin_usuario",
            defaults={
                "nombres": "Administrador",
                "apellidos": "Principal",
                "tipo_documento": "CC",
                "correo": "admin@altosdefontibon.com",
                "telefono": "123456789012",  # 12 dígitos, los primeros 7 fijos
                "celular": "3216549870",      # inventado
                "contraseña": "administradro.2025$",
                "id_rol": rol_admin,
                "estado": "Activo",
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS("✅ Usuario administrador creado correctamente"))
        else:
            self.stdout.write("⚠️ Usuario administrador ya existía")

        self.stdout.write(self.style.SUCCESS("\n🎉 Datos iniciales cargados correctamente"))
