from django.urls import re_path
from .consumers import *

websocket_urlpatterns = [
    re_path(r"ws/mis-reservas/(?P<usuario_id>\d+)/$", MisReservasConsumer.as_asgi()),
    re_path(r"ws/noticias/$", NoticiasConsumer.as_asgi()),
    re_path(
    r"ws/pago-residente/(?P<usuario_id>\d+)/(?P<reserva_id>\d+)/$",
    PagoReservaResidenteConsumer.as_asgi()
),
]
