from django.urls import re_path
from .consumers import *

websocket_urlpatterns = [
    re_path(r"ws/mis-reservas/(?P<usuario_id>\d+)/$", MisReservasConsumer.as_asgi()),
    re_path(r"ws/noticias/$", NoticiasConsumer.as_asgi()),
    re_path(r"ws/pagos-reserva-user/(?P<usuario_id>\d+)/(?P<reserva_id>\d+)/$", 
            PagosReservaResidenteConsumer.as_asgi()),
]
