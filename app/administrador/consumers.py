import json
from channels.generic.websocket import AsyncWebsocketConsumer

class UsuariosConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "usuarios_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def usuarios_update(self, event):
        await self.send(json.dumps(event))
        
        
class ReservasConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "reservas_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def reservas_update(self, event):
        await self.send(json.dumps(event))
        

class PagosReservaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.reserva_id = self.scope["url_route"]["kwargs"]["reserva_id"]
        self.group_name = f"pagos_reserva_{self.reserva_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def pagos_update(self, event):
        await self.send(json.dumps(event))



class VehiculosConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "vehiculos_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def vehiculos_update(self, event):
        # Envía el HTML renderizado al cliente
        await self.send(json.dumps(event))
