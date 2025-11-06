# usuarios/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string
from asgiref.sync import sync_to_async


class UsuariosConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("usuarios_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("usuarios_group", self.channel_name)

    async def receive(self, text_data):
        # No se recibe nada del cliente, solo se envía desde el servidor
        pass

    async def enviar_lista_usuarios(self, event):
        # Importamos dentro de la función (para evitar AppRegistryNotReady)
        from usuario.models import Usuario, Rol

        # Ejecutamos consultas de forma asíncrona segura
        usuarios = await sync_to_async(list)(
            Usuario.objects.select_related("id_rol").all()
        )
        roles = await sync_to_async(list)(Rol.objects.all())

        html = render_to_string("administrador/usuario/tabla_usuarios.html", {
            "usuarios": usuarios,
            "roles": roles
        })

        await self.send(text_data=json.dumps({
            "html": html
        }))
