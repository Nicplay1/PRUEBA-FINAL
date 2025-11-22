from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/usuarios/$", consumers.UsuariosConsumer.as_asgi()),
    re_path(r"ws/reservas/$", consumers.ReservasConsumer.as_asgi()),
    re_path(
    r"ws/pagos-reserva/(?P<reserva_id>\d+)/$",
    consumers.PagosReservaConsumer.as_asgi()
    ),
    re_path(r"ws/vehiculos/$", consumers.VehiculosConsumer.as_asgi()),
    re_path(
    r"ws/vehiculo-archivos/(?P<vehiculo_id>\d+)/$",
    consumers.ArchivosVehiculoConsumer.as_asgi()
    ),
    re_path(r"ws/novedades-admin/$", consumers.NovedadesAdminConsumer.as_asgi()),
]