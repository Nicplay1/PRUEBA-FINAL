from django.db import models
from django.utils import timezone
import uuid
from datetime import timedelta

# --------------------- ROL ---------------------
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'Rol'

    def __str__(self):
        return self.nombre_rol


# --------------------- USUARIO ---------------------
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    tipo_documento = models.CharField(
        max_length=20,
        choices=[('CC', 'CC'), ('CE', 'CE'), ('TI', 'TI'), ('Pasaporte', 'Pasaporte')]
    )
    numero_documento = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=13)
    celular = models.CharField(max_length=13)
    estado = models.CharField(max_length=10, default='Activo')
    contraseña = models.CharField(max_length=250, null=True, blank=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='ID_rol', default=1)
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    reset_token_expira = models.DateTimeField(null=True, blank=True)

    class Meta:
<<<<<<< Updated upstream
        db_table = "Usuario"   # <- Esto fuerza a Django a usar esa tabla
        managed = False  # <- Esto le dice a Django que NO maneje migraciones
        
=======
        managed = True
        db_table = "usuario"

>>>>>>> Stashed changes
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    def generar_token_reset(self):
        token = str(uuid.uuid4())
        self.reset_token = token
        self.reset_token_expira = timezone.now() + timedelta(hours=1)
        self.save()
        return token

    def token_es_valido(self, token):
        return (
            self.reset_token == token and
            self.reset_token_expira and
            timezone.now() < self.reset_token_expira
        )


# --------------------- ZONA COMUN ---------------------
class ZonaComun(models.Model):
    id_zona = models.AutoField(primary_key=True)
    nombre_zona = models.CharField(max_length=20)
    capacidad = models.IntegerField()
    tipo_pago = models.CharField(
        max_length=20,
        choices=[
            ('Por hora', 'Por hora'),
            ('Franja horaria', 'Franja horaria'),
            ('Evento', 'Evento')
        ]
    )
    estado = models.BooleanField(default=True)
    tarifa_base = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
<<<<<<< Updated upstream
        # Esto le indica a Django que la tabla ya existe y no debe crearla
        managed = False
        
        # Le dice a Django el nombre exacto de la tabla en la base de datos
        db_table = 'Zona_comun'
=======
        managed = True
        db_table = "zona_comun"
>>>>>>> Stashed changes

    def __str__(self):
        return self.nombre_zona


# --------------------- RESERVA ---------------------
class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(
        max_length=15,
        choices=[('Rechazada', 'Rechazada'), ('Aprobada', 'Aprobada'), ('En espera', 'En espera')],
        default='En espera'
    )
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_uso = models.DateField()
    observacion = models.CharField(max_length=255, null=True, blank=True)
    forma_pago = models.CharField(
        max_length=20,
        choices=[('Transferencia', 'Transferencia'), ('Efectivo', 'Efectivo')],
        null=True, blank=True
    )
    valor_pago = models.FloatField(null=True, blank=True)
    cod_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='cod_usuario')
    cod_zona = models.ForeignKey(ZonaComun, on_delete=models.CASCADE, db_column='cod_zona')

    class Meta:
<<<<<<< Updated upstream
        managed = False   # ⚠️ Recuerda que Django NO manejará migraciones aquí
        db_table = 'Reserva'
=======
        managed = True
        db_table = "reserva"
>>>>>>> Stashed changes

    def __str__(self):
        return f"Reserva {self.id_reserva} - {self.cod_usuario}"


# --------------------- DETALLE RESIDENTE ---------------------
class DetalleResidente(models.Model):
    id_detalle_residente = models.AutoField(primary_key=True)
    propietario = models.BooleanField(default=True)
    apartamento = models.IntegerField()
    torre = models.IntegerField()
    cod_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='cod_usuario')

    class Meta:
        managed = False
        db_table = 'Detalle_residente'

    def __str__(self):
        return f"Residente {self.cod_usuario} - Torre {self.torre}, Apto {self.apartamento}"


# --------------------- NOTICIAS ---------------------
class Noticias(models.Model):
    id_noticia = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    cod_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='cod_usuario')

    class Meta:
<<<<<<< Updated upstream
        managed = False   # porque la tabla ya existe en la BD
        db_table = 'Noticias'
=======
        managed = True
        db_table = "noticias"
>>>>>>> Stashed changes

    def __str__(self):
        return f"Noticia {self.id_noticia}: {self.descripcion[:30]}..."


# --------------------- VEHICULO RESIDENTE ---------------------
class VehiculoResidente(models.Model):
    id_vehiculo_residente = models.AutoField(primary_key=True, db_column='id_vehiculo_residente')
    placa = models.CharField(max_length=7, unique=True)
    tipo_vehiculo = models.CharField(
        max_length=10,
        choices=[('Carro', 'Carro'), ('Moto', 'Moto')]
    )
    activo = models.BooleanField()
    documentos = models.BooleanField(default=False)
    cod_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='cod_usuario')

    class Meta:
        managed = False
        db_table = 'Vehiculo_residente'

    def __str__(self):
        return f"{self.placa} - {self.tipo_vehiculo}"


# --------------------- TIPO ARCHIVO ---------------------
class TipoArchivo(models.Model):
    id_tipo_archivo = models.AutoField(primary_key=True, db_column='id_tipo_archivo')
    tipo_documento = models.CharField(
        max_length=50,
        choices=[('SOAT','SOAT'), ('Tarjeta de propiedad','Tarjeta de propiedad'),
                 ('Técnico-mecánica','Técnico-mecánica'), ('Licencia','Licencia'),
                 ('Identidad','Identidad')]
    )

    class Meta:
<<<<<<< Updated upstream
        managed = False
        db_table = 'TipoArchivo'
=======
        managed = True
        db_table = "tipo_archivo"
>>>>>>> Stashed changes

    def __str__(self):
        return self.tipo_documento


# --------------------- ARCHIVO VEHICULO ---------------------
class ArchivoVehiculo(models.Model):
    id_archivo = models.AutoField(primary_key=True, db_column='id_archivo')
    id_vehiculo = models.ForeignKey(VehiculoResidente, on_delete=models.CASCADE, db_column='id_vehiculo')
    id_tipo_archivo = models.ForeignKey(TipoArchivo, on_delete=models.CASCADE, db_column='id_tipo_archivo')
    ruta_archivo = models.CharField(max_length=255)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'ArchivoVehiculo'

    def __str__(self):
        return f"{self.id_vehiculo.placa} - {self.id_tipo_archivo.tipo_documento}"


# --------------------- PARQUEADERO ---------------------
class Parqueadero(models.Model):
    id_parqueadero = models.IntegerField(primary_key=True, db_column='id_parqueadero')
    numero_parqueadero = models.CharField(max_length=6)
    comunal = models.BooleanField()
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Parqueadero'

    def __str__(self):
        return f"Parqueadero {self.numero_parqueadero}"


# --------------------- SORTEO ---------------------
class Sorteo(models.Model):
<<<<<<< Updated upstream
    id_sorteo = models.AutoField(primary_key=True, db_column='ID_sorteo')
    fecha_creado = models.DateTimeField(auto_now_add=True, db_column='fecha_creado')
=======
    id_sorteo = models.AutoField(primary_key=True, db_column='id_sorteo')
    fecha_creado = models.DateTimeField(auto_now_add=True)
>>>>>>> Stashed changes
    tipo_residente_propietario = models.BooleanField(null=True, blank=True)
    fecha_inicio = models.DateField()
    hora_sorteo = models.TimeField(null=True, blank=True)
    estado = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'Sorteo'

    def __str__(self):
        tipo = "Propietarios" if self.tipo_residente_propietario else "Arrendatarios" if self.tipo_residente_propietario == False else "Todos"
        estado_text = "Realizado" if self.estado else "Pendiente"
        return f"Sorteo {self.id_sorteo} - {tipo} - {self.fecha_inicio} ({estado_text})"


# --------------------- GANADOR SORTEO ---------------------
class GanadorSorteo(models.Model):
    id_ganador = models.AutoField(primary_key=True, db_column='id_ganador')
    id_sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE, db_column='id_sorteo')
    id_detalle_residente = models.ForeignKey(DetalleResidente, on_delete=models.CASCADE, db_column='id_detalle_residente')
    id_parqueadero = models.ForeignKey(Parqueadero, on_delete=models.CASCADE, db_column='id_parqueadero')
    fecha_ganado = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'Ganador_sorteo'

    def __str__(self):
        return f"Ganador: {self.id_detalle_residente} - Parqueadero {self.id_parqueadero.numero_parqueadero}"


# --------------------- VISITANTE ---------------------
class Visitante(models.Model):
    id_visitante = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    documento = models.CharField(max_length=50)
    celular = models.CharField(max_length=20)
    tipo_vehiculo = models.CharField(max_length=20)
    placa = models.CharField(max_length=10)
    torre = models.CharField(max_length=10, null=True, blank=True)
    apartamento = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'visitante'

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.placa}"


# --------------------- DETALLES PARQUEADERO ---------------------
class DetallesParqueadero(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    tipo_propietario = models.CharField(
        max_length=10,
        choices=[('Visitante', 'Visitante'), ('Residente', 'Residente')]
    )
<<<<<<< Updated upstream
    id_visitante = models.ForeignKey(
        'Visitante',
        models.DO_NOTHING,
        db_column='id_visitante',
        blank=True,
        null=True
    )
    id_vehiculo_residente = models.ForeignKey(
        'VehiculoResidente',
        models.DO_NOTHING,
        db_column='id_vehiculo_residente',
        blank=True,
        null=True
    )
    registro = models.DateField(auto_now_add=True)  # fecha automática
    hora_llegada = models.TimeField(blank=True, null=True)
    hora_salida = models.TimeField(blank=True, null=True)
    pago = models.FloatField(blank=True, null=True)  # nuevo campo para el pago
    id_parqueadero = models.ForeignKey(
        'Parqueadero',
        models.DO_NOTHING,
        db_column='ID_parqueadero'
    )
=======
    id_visitante = models.ForeignKey(Visitante, on_delete=models.DO_NOTHING, db_column='id_visitante', null=True, blank=True)
    id_vehiculo_residente = models.ForeignKey(VehiculoResidente, on_delete=models.DO_NOTHING, db_column='id_vehiculo_residente', null=True, blank=True)
    registro = models.DateTimeField(auto_now_add=True)
    hora_llegada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)
    pago = models.FloatField(null=True, blank=True)
    id_parqueadero = models.ForeignKey(Parqueadero, on_delete=models.DO_NOTHING, db_column='id_parqueadero')
>>>>>>> Stashed changes

    class Meta:
        managed = False
        db_table = 'detalles_parqueadero'

    def __str__(self):
        return f"Detalle {self.id_detalle} - {self.tipo_propietario}"


# --------------------- REGISTRO CORRESPONDENCIA ---------------------
class RegistroCorrespondencia(models.Model):
    id_correspondencia = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10, choices=[('Recibo','Recibo')])
    descripcion = models.TextField()
    fecha_registro = models.DateTimeField()
    cod_vigilante = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, db_column='cod_vigilante', related_name='correspondencias_vigilante')

    class Meta:
<<<<<<< Updated upstream
        db_table = 'RegistroCorrespondencia'
        managed = False  # Django no intentará crear ni modificar la tabla
=======
        managed = True
        db_table = "registro_correspondencia"
>>>>>>> Stashed changes

    def __str__(self):
        return f"{self.tipo} - {self.descripcion[:20]}"


# --------------------- ENTREGA CORRESPONDENCIA ---------------------
class EntregaCorrespondencia(models.Model):
<<<<<<< Updated upstream
    id_Entrega = models.AutoField(primary_key=True)
    fechaEntrega = models.DateTimeField(auto_now_add=True)  # se llena automáticamente
    idUsuario = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        db_column='idUsuario',
        related_name='entregas_usuario'
    )
    idCorrespondecia = models.ForeignKey(
        RegistroCorrespondencia,
        on_delete=models.DO_NOTHING,
        db_column='idCorrespondecia',
        related_name='entregas_correspondencia'
    )
    idDetalles_residente = models.ForeignKey(
        'DetalleResidente',  # Asumiendo que tienes un modelo llamado DetalleResidente
        on_delete=models.DO_NOTHING,
        db_column='idDetalles_residente',
        related_name='entregas_residente'
    )

    class Meta:
        db_table = 'EntregaCorrespondecia'
        managed = False  # Django no intentará crear o modificar la tabla
=======
    id_entrega = models.AutoField(primary_key=True)
    fecha_entrega = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, db_column='id_usuario', related_name='entregas_usuario')
    id_correspondencia = models.ForeignKey(RegistroCorrespondencia, on_delete=models.DO_NOTHING, db_column='id_correspondencia', related_name='entregas_correspondencia')
    id_detalle_residente = models.ForeignKey(DetalleResidente, on_delete=models.DO_NOTHING, db_column='id_detalle_residente', related_name='entregas_residente')

    class Meta:
        managed = True
        db_table = "entrega_correspondencia"
>>>>>>> Stashed changes

    def __str__(self):
        return f"Entrega {self.id_entrega} - {self.id_detalle_residente}"


# --------------------- PAQUETE ---------------------
class Paquete(models.Model):
    id_paquete = models.AutoField(primary_key=True)
    apartamento = models.IntegerField()
    torre = models.IntegerField()
    fecha_recepcion = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    cod_usuario_recepcion = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='cod_usuario_recepcion', related_name='paquetes_recepcion')
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    cod_usuario_entrega = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='cod_usuario_entrega', null=True, blank=True, related_name='paquetes_entrega')
    nombre_residente = models.CharField(max_length=100, null=True, blank=True)
    foto_cedula = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = True
        db_table = "paquete"

    def __str__(self):
        return f"Paquete {self.id_paquete} - {self.nombre_residente}"


# --------------------- PAGOS RESERVA ---------------------
class PagosReserva(models.Model):
    id_pago = models.AutoField(primary_key=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    archivo_1 = models.FileField(upload_to='pagos/')
    archivo_2 = models.FileField(upload_to='pagos/', null=True, blank=True)
    estado = models.BooleanField(default=False)
    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, db_column='id_reserva')

    class Meta:
        managed = False
        db_table = 'pagos_reserva'

    def __str__(self):
        return f"Pago {self.id_pago} de la Reserva {self.id_reserva.id_reserva}"


# --------------------- NOVEDADES ---------------------
class Novedades(models.Model):
    id_novedad = models.AutoField(primary_key=True)
<<<<<<< Updated upstream
    descripcion = models.TextField(db_column='Descripcion')
    foto = models.FileField(upload_to='novedades/', null=True, blank=True)  # Cambio aquí
    fecha = models.DateTimeField(auto_now_add=True)
    
    id_detalle_residente = models.ForeignKey(
        'DetalleResidente',
        on_delete=models.DO_NOTHING,
        db_column='id_detalle_residente',
        null=True,
        blank=True
    )
    
    id_visitante = models.ForeignKey(
        'Visitante',
        on_delete=models.DO_NOTHING,
        db_column='id_visitante',
        null=True,
        blank=True
    )
    
    id_paquete = models.ForeignKey(
        'vigilante.Paquete',  # 👈 referencia la app correcta
        on_delete=models.DO_NOTHING,
        db_column='ID_paquete',
        null=True,
        blank=True
    )
    
    id_usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.DO_NOTHING,
        db_column='id_usuario',
        null=True,
        blank=True
    )
=======
    descripcion = models.TextField()
    foto = models.FileField(upload_to='novedades/', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    id_detalle_residente = models.ForeignKey(DetalleResidente, on_delete=models.DO_NOTHING, db_column='id_detalle_residente', null=True, blank=True)
    id_visitante = models.ForeignKey(Visitante, on_delete=models.DO_NOTHING, db_column='id_visitante', null=True, blank=True)
>>>>>>> Stashed changes

    class Meta:
        managed = False
        db_table = 'novedades'

    def __str__(self):
        return f"Novedad {self.id_novedad} - {self.descripcion[:20]}"
