from django.shortcuts import render


def index(request):
    return render(request, 'battle/chat.html')

def room(request, room_name):
    return render(request, 'battle/room.html', {
        'room_name': room_name
    })