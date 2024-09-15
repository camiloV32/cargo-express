from django.dispatch import receiver
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

from api.models import OrderProduct, Order
from .metrics import get_sales_metrics

@receiver(post_save, sender=Order)
@receiver(post_save, sender=OrderProduct)
def send_data_metrics(sender, instance, **kwargs):
    metrics = get_sales_metrics()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'data',
        {
            'type': 'send_metrics',
            'metrics': metrics
        }
    )

class monitoringApp(WebsocketConsumer):
    def connect(self):
        print('Conecxion establecida')
        async_to_sync(self.channel_layer.group_add)('data',self.channel_name)
        self.accept()
        self.send_initial_data()

        # return super().connect()
    def disconnect(self, code):
        print('Se ha desconectado')
        async_to_sync(self.channel_layer.group_discard)('data',self.channel_name)
        # return super().disconnect(code)

    def send_initial_data(self):
        metrics = get_sales_metrics()
        self.send(text_data=metrics)

    def send_metrics(self, event):
        # Obtener las métricas del evento
        metrics = event['metrics']
        
        # Enviar los datos al cliente WebSocket
        self.send(text_data=metrics)


    
