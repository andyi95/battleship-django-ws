# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from chat.models import Ship, Board

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.board, created = Board.objects.get_or_create(name=str(self.room_name))
        brd_arr = self.board.full_board()
        brd_str = '\n ' + ' '.join(str(x) for x in range(1, 10))
        for r in range(10):
            brd_str+=str(r+1) + ' ' + ' '.join(str(c) for c in brd_arr[r])
            brd_str+='\n'
        self.accept()

        self.send(text_data=json.dumps({'message': 'Welcome to the Internet!'}))
        s = self.board.new_ship('horizontal', [2, 3], 4)
        s1 = self.board.new_ship('vertical', [1, 5], 2)
        s2 = self.board.new_ship('vertical', [8, 1], 5)
        s3 = self.board.new_ship('vertical', [6, 1], 5)
        self.board.check_for_hit([3,3])
        self.send(text_data=json.dumps({'message': brd_str}))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': f'message is {message}'
        }))
        message = message.split(' ')
        ans = self.board.shot(message)
        self.send(text_data=json.dumps({'message': ans}))
        brd_arr = self.board.full_board()
        brd_str = '\n ' + ' '.join(str(x) for x in range(1, 10))
        for r in range(10):
            brd_str += str(r + 1) + ' ' + ' '.join(str(c) for c in brd_arr[r])
            brd_str += '\n'
        self.send(text_data=json.dumps({'message': brd_str}))

# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
#
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         self.accept()
#
#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))
