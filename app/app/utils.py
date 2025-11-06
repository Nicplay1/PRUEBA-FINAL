from django.template.loader import render_to_string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from usuario.models import *

def enviar_noticias_ws():
    noticias = Noticias.objects.all().order_by("-fecha_publicacion")

    html = render_to_string(
        "residente/detalles_residente/_noticias_list.html",
        {"noticias": noticias}
    )

    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        "noticias_updates",
        {
            "type": "send_update",
            "data": {
                "html": html,
                "mensaje": "Noticias actualizadas!"
            },
        }
    )
