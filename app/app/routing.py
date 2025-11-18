from django.urls import path,re_path
from .consumers import *
from residente.consumers import *
from administrador.consumers import *

websocket_urlpatterns = [
    # ruta para el panel administrador
    path("ws/usuarios/", UsuariosConsumer.as_asgi()),
    path("ws/reservas/", ReservasConsumer.as_asgi()),
    path("ws/mis-reservas/<int:usuario_id>/", MisReservasConsumer.as_asgi()),
    path("ws/noticias/", NoticiasConsumer.as_asgi()),
    
]
