from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from usuario.models import *


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
# PAGOS — ADMIN
# ------------------------------

def enviar_pagos_update(instance, action):
    channel_layer = get_channel_layer()
    reserva_id = instance.id_reserva.id_reserva

    pagos = PagosReserva.objects.filter(id_reserva=instance.id_reserva).order_by("-id_pago")

    html = render_to_string("administrador/reservas/tabla_pagos_reserva.html", {
        "pagos": pagos
    })

    async_to_sync(channel_layer.group_send)(
        f"pagos_reserva_{reserva_id}",
        {
            "type": "pagos_update",
            "action": action,
            "html": html
        }
    )


# ------------------------------
# PAGOS — RESIDENTE
# ------------------------------

def enviar_pagos_residente_update(instance, action):
    channel_layer = get_channel_layer()

    usuario_id = instance.id_reserva.cod_usuario.id_usuario
    reserva_id = instance.id_reserva.id_reserva

    pagos = PagosReserva.objects.filter(id_reserva=instance.id_reserva).order_by("-id_pago")

    html = render_to_string("residente/zonas_comunes/tabla_pagos_residente.html", {
        "pagos": pagos
    })

    async_to_sync(channel_layer.group_send)(
        f"pagos_reserva_user_{usuario_id}_{reserva_id}",
        {
            "type": "pagos_update",
            "action": action,
            "html": html
        }
    )


# ------------------------------
# UNIFICAR SEÑALES
# ------------------------------

@receiver(post_save, sender=PagosReserva)
def pago_guardado(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    enviar_pagos_update(instance, action)
    enviar_pagos_residente_update(instance, action)


@receiver(post_delete, sender=PagosReserva)
def pago_eliminado(sender, instance, **kwargs):
    enviar_pagos_update(instance, "deleted")
    enviar_pagos_residente_update(instance, "deleted")
