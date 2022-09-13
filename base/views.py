from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm

# Create your views here.

#function base views
def home(request):
    rooms = Room.objects.all()
    context = { 'rooms': rooms }
    return render(request, 'base/home.html', context )

def room(request, pk):
    room = Room.objects.get(id=pk)
    # for room in rooms:
    #     if room['id'] == pk:
    #         return room
    context = {'room': room}

    return render(request, 'base/room.html', context)


# This handles the form rendering - CREATING 

def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


# This handles the uodating request - UPDATING

def update_room(request, pk):
    # NB the pk lets you know the item we are updating. in this case, I am using the pk or id.
    room = Room.objects.get(id=pk)

    form = RoomForm(instance=room) # get the form content that have the instance of the form

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = { 'form': form }
    return render(request, 'base/room_form.html', context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    return render(request, 'base/delete_form.html', {'obj': room})
    