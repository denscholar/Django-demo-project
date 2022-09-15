from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RoomForm



# Login functionality
def login_page(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        # Get the user username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user exist and if not, a flash message will display on the screen according to django documentation
        try:
            user =  user.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        # Authenticate the user if the user exist but ensure you inport the authenticate and login built-in method

        user = authenticate(request, username=username, password=password)

        if user is not None: # if user exist in the database
            login(request, user) # logs in the user by calling the django built-in login method 
            return redirect('home') # redirects the user to home after succesfully logs in
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {}
    return render(request, 'base/login.html', context)

# Log out functionality
def logout_user(request):
    logout(request)
    return redirect('home')


#function base views
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
    ) # all the rooms based on the query

    topics = Topic.objects.all() #all the topics
    room_count = rooms.count()

    context = { 'rooms': rooms, 'topics': topics, 'room_count': room_count }

    return render(request, 'base/home.html', context )


# get a single room
def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}

    return render(request, 'base/room.html', context)


# This handles the form rendering - CREATING
@login_required(login_url = '/login')
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
@login_required(login_url = '/login')
def update_room(request, pk):
    # NB the pk lets you know the item we are updating. in this case, I am using the pk or id.
    room = Room.objects.get(id=pk)

    form = RoomForm(instance=room) # get the form content that have the instance of the form

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = { 'form': form }
    return render(request, 'base/room_form.html', context)

# Deleting  A ROOM
@login_required(login_url = '/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    return render(request, 'base/delete_form.html', {'obj': room})
    