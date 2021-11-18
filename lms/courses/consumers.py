  
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser





class ChatConsumer(WebsocketConsumer):
    def connect(self):
        #user_id = (self.scope["query_string"].decode("utf-8")).split('=')[1]
    
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.group_name= 'room_%s' % self.room_name
        
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
        
        data = {'type' : 'connected' }
        
        async_to_sync(self.channel_layer.group_send)(
                'room_%s' % self.room_name,{
                    'type':'send_online_status',
                    'value': json.dumps(data),
            }
        )
        
        self.send(text_data=json.dumps({
            'payload': 'connected',
        }))
        
    def disconnect(self,close_code):
        
        data = {'type' : 'connected' }
        
        async_to_sync(self.channel_layer.group_send)(
                'room_%s' % self.room_name,{
                    'type':'send_online_status',
                    'value': json.dumps(data),
                    
            }
        )
        
        
        
    
    def receive(self,text_data):
        data = json.loads(text_data)
        
        data['type'] = 'message'
        
        async_to_sync(self.channel_layer.group_send)(
                'room_%s' % self.room_name,{
                    'type':'send_message',
                    'value': json.dumps(data),
            }
        )
        
    def send_message(self , text_data):
        data = json.loads(text_data['value']) 
        self.send(text_data = json.dumps({
            'payload': data
        }))
        
        
    def send_online_status(self , text_data):
        data = json.loads(text_data['value']) 
    
        
        
        self.send(text_data = json.dumps({
            'payload': data
        }))
  