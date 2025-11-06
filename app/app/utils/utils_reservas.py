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
