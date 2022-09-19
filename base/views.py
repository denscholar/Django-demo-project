from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RoomForm



# Login functionality
def login_page(request):
    page = 'Login Page'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        # Get the user username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user exist and if not, a flash message will display on the screen according to django documentation
        
        # try:
        #     user =  user.objects.get(username=username)
        # except:
        #     messages.error(request, 'User does not exist')

        # Authenticate the user if the user exist but ensure you inport the authenticate and login built-in method

        user = authenticate(request, username=username, password=password)

        if user is not None: # if user exist in the database
            login(request, user) # logs in the user by calling the django built-in login method 
            return redirect('home') # redirects the user to home after succesfully logs in
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page': page}
    return render(request, 'base/login.html', context)

# Log out functionality
def logout_user(request):
    logout(request)
    return redirect('home')

# Registeration for new user
def register_user(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Clean the data in case for any uppercase data
            user.username = user.username.lower()
            user.save()

            # Log the user in by calling the django built-in login method

            login(request, user)

            # Redirect to the home page after login in

            return redirect('home')

        else:
            messages.error(request, 'An error occure during registration')

    context = {'form': form}
    return render(request, 'base/login.html', context)


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

    room_messages = Message.objects.all().order_by('-created').filter(Q(room__topic__name__icontains=q))

    context = { 'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages }

    return render(request, 'base/home.html', context )


# get a single room
def room(request, pk):
    room = Room.objects.get(id=pk)

    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)



    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics }
    return render(request, 'base/profile.html', context)



# This handles the form rendering - CREATING
@login_required(login_url = '/login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
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


@login_required(login_url = '/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
        
    return render(request, 'base/delete_form.html', {'obj': message})
    