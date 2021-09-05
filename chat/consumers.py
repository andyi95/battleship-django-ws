import json
from channels.generic.websocket import WebsocketConsumer
from chat.models import Ship, Board
import re

SYM = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'L']
class ChatConsumer(WebsocketConsumer):

    def print_board(self, board):
        brd_arr = board.full_board()
        brd_str = '\n ' + ' '.join(str(x) for x in range(1, 11))+'\n'
        for r in range(10):
            brd_str+=SYM[r] + ' ' + ' '.join(str(c) for c in brd_arr[r])+'\n'
        return brd_str

    def new_ships(self):
        ships = 0
        while(ships<4):
            s = self.board.build_ships()
            if s is not None:
                ships+=1
                s = None
        brd_str = self.print_board(self.board)
        return brd_str

    def command(self, command):
        if command == '/restart':
            self.board.delete()
            self.board = Board.objects.create(name=self.room_name)
            self.new_ships()
            msg = self.print_board(self.board)
            self.send(text_data=json.dumps({'message': msg}))
        else:
            self.send(text_data=json.dumps({'message': 'command not found'}))


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.board, created = Board.objects.get_or_create(
            name=self.room_name
        )
        self.accept()
        self.send(text_data=json.dumps(
            {'message': 'Welcome to the Internet!'})
        )
        brd_str = self.new_ships()
        self.send(text_data=json.dumps({'message': brd_str}))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': f'message is {message}'
        }))
        if message.startswith('/'):
            self.command(message)
        message = re.findall('(\d+|\D+)', message)
        if len(message) == 2:
            r = SYM.index(message[0])
            ans = self.board.shot([message[1], r])
            self.send(text_data=json.dumps({'message': ans}))
            brd_str = self.print_board(self.board)
        else:
            brd_str = 'Got a wrong message'
        self.send(text_data=json.dumps({'message': brd_str}))
