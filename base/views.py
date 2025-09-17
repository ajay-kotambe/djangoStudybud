# for render and redirect to redirect or render the pages
from django.shortcuts import render, redirect
# 
from django.http import HttpResponse
# models from .models
from .models import Room, Topic
# 
from django.db.models import Q
# importing RoomForm from .forms
from .forms import RoomForm
# for creating user from default django user
from django.contrib.auth.models import User
# for splash messages
from django.contrib import messages
# for restrictions
from django.contrib.auth.decorators import login_required
#  for authentications
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm



# Create your views here.

rooms = [
    {"id": 1, "name": "Lets Learn Python! "},
    {"id": 2, "name": "Desgin with me "},
    {"id": 3, "name": "Frontend Developersf"},
]

def logoutUser(request):
    logout(request)
    return redirect('homePage')
    

def loginPage(request):
    page = 'loginPage'
    if request.user.is_authenticated:
        messages.error(request,"You are already logged in..!")
        return redirect('homePage')
    
    if request.method == 'POST':
        username =  request.POST.get('username').lower()
        password =  request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User doesn't exist")
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('homePage')
        else :
            messages.error(request,"Usernamer or password is incorrect")
    context = {'page':page}
    return render(request, 'base/loginRegister.html',context)

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('homePage')
        else:
            messages.error(request, "An occurred during registartion ")
            
    context = {'form':form}
    return render(request, 'base/loginRegister.html',context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 
    rooms = Room.objects.filter(Q(topic__name__contains= q) |
                                Q(name__contains = q) |
                                Q(description__contains = q))
    
    # q = request.GET.get('q')  
    # if q:  
    #     rooms = Room.objects.filter(topic__name__icontains=q)
    # else:  
    #     rooms = Room.objects.all()
    
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {"rooms": rooms, "topics":topics,"count":room_count}
    return render(request, "base/home.html", context)

@login_required(login_url='loginPage')
def room(request, pk):
    room = Room.objects.get(id=pk)
    roomMessages = room.message_set.all()
    rooms = Room.objects.get(id=pk)
    # print(type(rooms))
    room = Room.objects.get(id=pk)

    context = {"room": room,'roomMessages':roomMessages}
    return render(request, "base/room.html", context)

@login_required(login_url='loginPage')
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("homePage")
        # request.POST.get('name') # if without ModelForm
    context = {"form": form}
    return render(request, "base/roomForm.html", context)

@login_required(login_url='loginPage')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are not allowed to edit this room..!')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('homePage')
    context = {'form':form}
    return render(request,"base/roomForm.html",context)

@login_required(login_url='loginPage')   
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk) 
    if request.user != room.host:
        return HttpResponse('You are not allowed to delete this room..!')
    if request.method == 'POST':
        room.delete()
        return redirect('homePage')
    return render(request,'base/delete.html',{'obj':room})