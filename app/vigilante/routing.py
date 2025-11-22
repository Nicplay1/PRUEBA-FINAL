from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/paquetes/$", consumers.PaquetesConsumer.as_asgi()),
    re_path(r"ws/parqueadero/$", consumers.ParqueaderoConsumer.as_asgi()),
     re_path(r"ws/correspondencia/$", consumers.CorrespondenciaConsumer.as_asgi()),
     re_path(r"ws/novedades/$", consumers.NovedadesConsumer.as_asgi()),
]
