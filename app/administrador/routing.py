from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/usuarios/$", consumers.UsuariosConsumer.as_asgi()),
    re_path(r"ws/reservas/$", consumers.ReservasConsumer.as_asgi()),
    re_path(
    r"ws/pagos-reserva/(?P<reserva_id>\d+)/$",
    consumers.PagosReservaConsumer.as_asgi()
),
]
