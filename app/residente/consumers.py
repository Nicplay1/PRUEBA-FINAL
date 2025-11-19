import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MisReservasConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        usuario_id = self.scope["url_route"]["kwargs"]["usuario_id"]
        self.group_name = f"mis_reservas_{usuario_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def reservas_update(self, event):
        await self.send(json.dumps(event))

class NoticiasConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "noticias_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def noticias_update(self, event):
        await self.send(json.dumps(event))
        
class PagoReservaResidenteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.reserva_id = self.scope["url_route"]["kwargs"]["reserva_id"]
        self.usuario_id = self.scope["url_route"]["kwargs"]["usuario_id"]
        self.group_name = f"pago_residente_{self.usuario_id}_{self.reserva_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def pago_residente_update(self, event):
        await self.send(json.dumps(event))

