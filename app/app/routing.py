from django.urls import path,re_path
from .consumers import *

websocket_urlpatterns = [
    # ruta para el panel administrador
    path("ws/usuarios/", AdminUserConsumer.as_asgi()),
    path("ws/noticias/", NoticiasConsumer.as_asgi()),
    path("ws/reservas/", ReservasConsumer.as_asgi()),
    path("ws/pagos/<int:reserva_id>/", PagosConsumer.as_asgi())
]
