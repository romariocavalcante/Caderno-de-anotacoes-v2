import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import *

class AnotacoesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtém o ID do cliente a partir da URL
        self.cliente_id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'cliente_{self.cliente_id}'

        # Cria o grupo para esse cliente específico
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove o cliente do grupo ao desconectar
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Recebe os dados do WebSocket
        data = json.loads(text_data)
        observacao = data.get('observacao', '')

        # Salva a observação no banco de dados
        cliente = get_object_or_404(Cliente, id=self.cliente_id)
        cliente.observacao = observacao
        cliente.save()

        # Envia a observação para todos os clientes conectados ao grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_observacao',
                'observacao': observacao
            }
        )

    async def send_observacao(self, event):
        # Envia a observação para o WebSocket do cliente
        observacao = event['observacao']
        await self.send(text_data=json.dumps({
            'observacao': observacao
        }))
