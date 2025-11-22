import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

# IMPORTA TODAS LAS RUTAS
import administrador.routing
import residente.routing
import vigilante.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

django_asgi_app = get_asgi_application()

# UNIFICAR TODAS LAS RUTAS WEBSOCKET
websocket_routes = (
    administrador.routing.websocket_urlpatterns +
    residente.routing.websocket_urlpatterns +
    vigilante.routing.websocket_urlpatterns 
)

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(websocket_routes),
})
