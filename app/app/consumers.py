import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AdminUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Todos los clientes que se conecten a esta ruta formarán parte del grupo 'admin_updates'
        self.group_name = "admin_updates"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Nombre del handler debe coincidir con "type" que envíes desde el servidor (ej: 'user.registered')
    async def user_registered(self, event):
        # event puede tener: html, mensaje, count (todo lo que quieras)
        payload = {
            "html": event.get("html", ""),
            "mensaje": event.get("mensaje", ""),
            "count": event.get("count", None)
        }
        await self.send(text_data=json.dumps(payload))
        
        


class NoticiasConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("noticias_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("noticias_updates", self.channel_name)

    async def send_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))

