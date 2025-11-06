from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    # ruta para el panel administrador
    path("ws/usuarios/", AdminUserConsumer.as_asgi()),
    path("ws/noticias/", NoticiasConsumer.as_asgi()),
    path("ws/reservas/", ReservasConsumer.as_asgi()),
]
