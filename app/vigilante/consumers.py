import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PaquetesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "paquetes_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def paquetes_update(self, event):
        # Enviar solo el HTML necesario
        await self.send(text_data=json.dumps({
            "html": event["html"]
        }))
        
class ParqueaderoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "parqueadero_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def parqueadero_update(self, event):
        await self.send(text_data=json.dumps({
            "html": event["html"]
        }))
        

class CorrespondenciaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "correspondencia_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def correspondencia_update(self, event):
        await self.send(text_data=json.dumps({
            "html": event["html"]
        }))
        
class NovedadesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "novedades_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def novedades_update(self, event):
        await self.send(text_data=json.dumps({
            "html": event["html"]
        }))