from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

rooms = [
    {'id': 1, 'name': 'Come lets learn python together'},
    {'id': 2, 'name': 'Come lets learn design'},
    {'id': 3, 'name': 'Come lets frontend Development'},
    {'id': 4, 'name': 'Come lets learn javascript'}
]

#function base views
def home(request):
    context = { 'rooms': rooms }
    return render(request, 'base/home.html', context )

def room(request, pk):
    room = None
    for room in rooms:
        if room['id'] == pk:
            return room
    context = {'room': room}

    return render(request, 'base/room.html', context)