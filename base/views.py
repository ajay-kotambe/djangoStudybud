from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from django.db.models import Q
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout



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
    
    if request.method == 'POST':
        username =  request.POST.get('username')
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

        
        
    context = {}
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


def room(request, pk):
    rooms = Room.objects.get(id=pk)
    # print(type(rooms))
    room = Room.objects.get(id=pk)

    # for i in rooms:
    #     if i["id"] == int(pk):
    #         room = i
    context = {"room": room}

    return render(request, "base/room.html", context)


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


def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('homePage')
    context = {'form':form}
    return render(request,"base/roomForm.html",context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk) 
    if request.method == 'POST':
        room.delete()
        return redirect('homePage')
    return render(request,'base/delete.html',{'obj':room})