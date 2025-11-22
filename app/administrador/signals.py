from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from usuario.models import *
from vigilante.models import *
from datetime import datetime, date, timedelta


# ------------------------------
# USUARIOS
# ------------------------------

@receiver(post_save, sender=Usuario)
def usuario_post_save(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    usuarios = Usuario.objects.select_related("id_rol").all()
    roles = Rol.objects.all()
    html = render_to_string("administrador/usuario/tabla_usuarios.html", {
        "usuarios": usuarios,
        "roles": roles
    })

    async_to_sync(channel_layer.group_send)(
        "usuarios_group",
        {
            "type": "usuarios_update",
            "action": "refresh",
            "html": html,
            "created": created,
            "usuario_id": instance.id_usuario,
            "nombres": instance.nombres,
            "apellidos": instance.apellidos,
        }
    )


# ------------------------------
# RESERVAS — ADMINISTRADOR
# ------------------------------

def enviar_reservas_update(action, instance):
    channel_layer = get_channel_layer()

    reservas = Reserva.objects.select_related("cod_usuario", "cod_zona").all().order_by("-fecha_reserva")

    html = render_to_string("administrador/reservas/tabla_reservas.html", {
        "reservas": reservas
    })

    async_to_sync(channel_layer.group_send)(
        "reservas_group",
        {
            "type": "reservas_update",
            "action": action,
            "html": html,
            "reserva_id": instance.id_reserva
        }
    )


# ------------------------------
# RESERVAS — RESIDENTE
# ------------------------------

def enviar_reservas_a_residente(instance, action):
    channel_layer = get_channel_layer()
    usuario_id = instance.cod_usuario.id_usuario

    reservas_usuario = Reserva.objects.filter(cod_usuario=instance.cod_usuario) \
                                     .select_related("cod_zona") \
                                     .order_by("-fecha_reserva")

    html = render_to_string("residente/zonas_comunes/tabla_mis_reservas.html", {
        "reservas": reservas_usuario
    })

    async_to_sync(channel_layer.group_send)(
        f"mis_reservas_{usuario_id}",
        {
            "type": "reservas_update",
            "action": action,
            "html": html,
            "reserva_id": instance.id_reserva
        }
    )


@receiver(post_save, sender=Reserva)
def reserva_creada_o_editada(sender, instance, created, **kwargs):
    enviar_reservas_update("created" if created else "updated", instance)
    enviar_reservas_a_residente(instance, "created" if created else "updated")


@receiver(post_delete, sender=Reserva)
def reserva_eliminada(sender, instance, **kwargs):
    enviar_reservas_update("deleted", instance)
    enviar_reservas_a_residente(instance, "deleted",)


# ------------------------------
# NOTICIAS
# ------------------------------

def enviar_noticias_update(action):
    channel_layer = get_channel_layer()
    noticias_list = Noticias.objects.all().order_by('-fecha_publicacion')

    html = render_to_string("residente/detalles_residente/tabla_noticias.html", {
        "noticias": noticias_list
    })

    async_to_sync(channel_layer.group_send)(
        "noticias_group",
        {
            "type": "noticias_update",
            "action": action,
            "html": html
        }
    )


@receiver(post_save, sender=Noticias)
def noticia_creada_o_editada(sender, instance, created, **kwargs):
    enviar_noticias_update("created" if created else "updated")


@receiver(post_delete, sender=Noticias)
def noticia_eliminada(sender, instance, **kwargs):
    enviar_noticias_update("deleted")

# ------------------------------
# PAGOS
# ------------------------------
def enviar_pago_a_residente(instance):
    channel_layer = get_channel_layer()

    reserva = instance.id_reserva
    usuario_id = reserva.cod_usuario.id_usuario

    # Renderizar el fragmento que se actualizará
    html = render_to_string("residente/zonas_comunes/tabla_pagos_residente.html", {
        "reserva": reserva,
        "pago": instance,
        "bloqueado": instance.estado in ["Aprobado", "Rechazado"],
        "nombre_archivo_1": instance.archivo_1.name if instance.archivo_1 else None,
        "nombre_archivo_2": instance.archivo_2.name if instance.archivo_2 else None,
    })

    async_to_sync(channel_layer.group_send)(
        f"pago_residente_{usuario_id}_{reserva.id_reserva}",
        {
            "type": "pago_residente_update",
            "action": "refresh",
            "html": html
        }
    )



@receiver(post_save, sender=PagosReserva)
def pago_creado_o_actualizado(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    reserva = instance.id_reserva

    pagos = PagosReserva.objects.filter(id_reserva=reserva)

    html = render_to_string("administrador/reservas/tabla_pagos_reserva.html", {
        "pagos": pagos
    })

    async_to_sync(channel_layer.group_send)(
        f"pagos_reserva_{reserva.id_reserva}",
        {
            "type": "pagos_update",
            "action": "refresh",
            "html": html
        }
    )
    enviar_pago_a_residente(instance)


def enviar_sorteos_a_residente(usuario):
    channel_layer = get_channel_layer()
    detalle = DetalleResidente.objects.filter(cod_usuario=usuario).first()

    if not detalle:
        return

    # Obtener si el residente tiene documentos válidos
    vehiculo = VehiculoResidente.objects.filter(cod_usuario=usuario).first()
    tiene_docs = vehiculo.documentos if vehiculo else False

    # Filtrar por tipo de residente
    if detalle.propietario:
        sorteos = Sorteo.objects.filter(tipo_residente_propietario=True).order_by('-id_sorteo')
    else:
        sorteos = Sorteo.objects.filter(tipo_residente_propietario=False).order_by('-id_sorteo')

    hoy = date.today()

    sorteos_info = []
    for sorteo in sorteos:
        participo = GanadorSorteo.objects.filter(
            id_sorteo=sorteo,
            id_detalle_residente__cod_usuario=usuario
        ).exists()

        gano = participo

        # Lógica corregida
        if participo or gano:
            participa = True
        elif sorteo.fecha_inicio > hoy and not tiene_docs:
            participa = False
        elif sorteo.fecha_inicio > hoy and tiene_docs:
            participa = True
        else:
            participa = False

        sorteos_info.append({
            "sorteo": sorteo,
            "participa": participa,
            "gano": gano
        })

    html = render_to_string("residente/sorteo/tabla_sorteos.html", {
        "sorteos_info": sorteos_info,
        "detalle_residente": detalle
    })

    async_to_sync(channel_layer.group_send)(
        f"mis_sorteos_{usuario.id_usuario}",
        {
            "type": "sorteos_update",
            "action": "refresh",
            "html": html
        }
    )

@receiver(post_save, sender=Sorteo)
def sorteo_creado(sender, instance, created, **kwargs):
    if created:
        # Enviar actualización a TODOS los residentes
        for usuario in Usuario.objects.filter(id_rol__nombre_rol="Residente"):
            enviar_sorteos_a_residente(usuario)




@receiver(post_save, sender=VehiculoResidente)
def vehiculo_creado_o_actualizado(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    # ----------------------------
    # 1. Actualizar tabla admin
    # ----------------------------
    vehiculos = VehiculoResidente.objects.all()

    html = render_to_string("administrador/vehiculos/tabla_vehiculos.html", {
        "vehiculos": vehiculos
    })

    async_to_sync(channel_layer.group_send)(
        "vehiculos_group",
        {
            "type": "vehiculos_update",
            "action": "refresh",
            "html": html,
        }
    )

    # ----------------------------
    # 2. ACTUALIZAR SORTEOS DEL RESIDENTE
    # ----------------------------
    enviar_sorteos_a_residente(instance.cod_usuario)

    
@receiver(post_save, sender=ArchivoVehiculo)
def archivo_guardado(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    vehiculo = instance.id_vehiculo
    archivos = ArchivoVehiculo.objects.filter(id_vehiculo=vehiculo)

    html = render_to_string("administrador/vehiculos/tabla_archivos.html", {
        "archivos": archivos
    })

    async_to_sync(channel_layer.group_send)(
        f"archivos_vehiculo_{vehiculo.id_vehiculo_residente}",
        {
            "type": "archivos_update",
            "html": html,
            "action": "refresh"
        }
    )


    
@receiver(post_save, sender=Paquete)
def actualizar_tabla_paquetes(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    html = render_to_string(
        "vigilante/correspondecia/tabla_paquetes.html",
        {"paquetes": Paquete.objects.all()},
    )

    async_to_sync(channel_layer.group_send)(
        "paquetes_group",
        {
            "type": "paquetes_update",
            "html": html
        }
    )
    
@receiver(post_save, sender=DetallesParqueadero)
@receiver(post_delete, sender=DetallesParqueadero)
def actualizar_tabla_parqueadero(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    
    # Obtener todos los registros con las relaciones necesarias
    registros = DetallesParqueadero.objects.select_related(
        "id_visitante", "id_vehiculo_residente", "id_parqueadero"
    ).order_by('-id_detalle')

    # Calcular tiempos y valores (igual que en la vista)
    for detalle in registros:
        if detalle.tipo_propietario == "Residente":
            detalle.valor_pago = 0
            detalle.tiempo_total = None
        elif detalle.hora_llegada and detalle.hora_salida:
            llegada_dt = datetime.combine(detalle.registro, detalle.hora_llegada)
            salida_dt = datetime.combine(detalle.registro, detalle.hora_salida)

            if salida_dt < llegada_dt:
                salida_dt += timedelta(days=1)

            duracion = salida_dt - llegada_dt
            horas = duracion.total_seconds() / 3600
            total_seconds = int(duracion.total_seconds())
            horas_int = total_seconds // 3600
            minutos_int = (total_seconds % 3600) // 60
            segundos_int = total_seconds % 60
            detalle.tiempo_total_str = f"{horas_int:02d}:{minutos_int:02d}:{segundos_int:02d}"
            detalle.valor_pago = round(max(horas, 1) * 2000, 2)
        else:
            detalle.tiempo_total = None
            detalle.valor_pago = None

    html = render_to_string(
        "vigilante/parqueadero/tabla_parqueadero.html",
        {"registros": registros},
    )

    async_to_sync(channel_layer.group_send)(
        "parqueadero_group",
        {
            "type": "parqueadero_update",
            "html": html
        }
    )
    
    
@receiver(post_save, sender=RegistroCorrespondencia)
def actualizar_tabla_correspondencia(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    
    registros = RegistroCorrespondencia.objects.all()
    html = render_to_string(
        "vigilante/correspondecia/partial_registros_correspondencia.html",
        {"registros": registros},
    )

    async_to_sync(channel_layer.group_send)(
        "correspondencia_group",
        {
            "type": "correspondencia_update",
            "html": html
        }
    )
    
@receiver(post_save, sender=Novedades)
@receiver(post_delete, sender=Novedades)
def actualizar_tabla_novedades(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    # Obtener todas las novedades con las relaciones necesarias
    novedades = Novedades.objects.select_related(
        "id_detalle_residente__cod_usuario",
        "id_visitante", 
        "id_paquete",
        "id_usuario"
    ).all().order_by('-fecha')

    html = render_to_string(
        "vigilante/novedades/tabla_novedades.html",
        {"novedades": novedades},
    )

    async_to_sync(channel_layer.group_send)(
        "novedades_group",
        {
            "type": "novedades_update",
            "html": html
        }
    )
    
@receiver(post_save, sender=Novedades)
@receiver(post_delete, sender=Novedades)
def actualizar_tabla_novedades_admin(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    # Obtener el filtro actual (simulando el comportamiento de la vista)
    filtro_actual = 'todos'  # Puedes ajustar esto según tu lógica de filtros
    
    # Obtener todas las novedades con las relaciones necesarias
    novedades = Novedades.objects.select_related(
        "id_visitante", 
        "id_paquete"
    ).all().order_by('-fecha')

    # Aplicar filtros si es necesario
    if hasattr(instance, '_filtro_actual'):
        filtro_actual = instance._filtro_actual

    if filtro_actual == 'visitante':
        novedades = novedades.filter(id_visitante__isnull=False)
    elif filtro_actual == 'paquete':
        novedades = novedades.filter(id_paquete__isnull=False)

    html = render_to_string(
        "administrador/novedades/tabla_novedades.html",
        {
            "novedades": novedades,
            "filtro_actual": filtro_actual
        },
    )

    async_to_sync(channel_layer.group_send)(
        "novedades_admin_group",
        {
            "type": "novedades_admin_update",
            "html": html
        }
    )