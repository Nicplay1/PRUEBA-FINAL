from django.template.loader import render_to_string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from usuario.models import *

def enviar_reservas_ws():
    reservas = Reserva.objects.select_related("cod_usuario", "cod_zona").all().order_by("-fecha_reserva")

    html = render_to_string(
        "administrador/reservas/tabla_reservas.html",
        {"reservas": reservas}
    )

    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        "reservas_updates",
        {
            "type": "send_update",
            "data": {
                "html": html,
                "mensaje": "Nueva actualización en reservas"
            },
        }
    )
    
def enviar_pago_reserva_ws(reserva):
    pagos = PagosReserva.objects.filter(id_reserva=reserva).order_by("-id_pago")

    html_pag_admin = render_to_string(
        "administrador/reservas/detalle_reserva_pagos.html",
        {"pagos": pagos}
    )

    html_residente = render_to_string(
        "residente/zonas_comunes/detalle_reserva.html",
        {"reservas": Reserva.objects.filter(cod_usuario=reserva.cod_usuario)}
    )

    layer = get_channel_layer()

    async_to_sync(layer.group_send)(
        f"reserva_{reserva.id_reserva}",
        {
            "type": "send_update",
            "data": {
                "html_pagos": html_pag_admin,
                "html_residente": html_residente,
            },
        }
    )

    async_to_sync(layer.group_send)(
        "pagos_updates",
        {
            "type": "send_update",
            "data": {
                "html_pagos": html_pag_admin,
                "reserva": reserva.id_reserva,
            },
        }
    )
