# for render and redirect to redirect or render the pages
from django.shortcuts import render, redirect
# 
from django.http import HttpResponse
# models from .models
from .models import Room, Topic, Message, User
# 
from django.db.models import Q
# importing RoomForm from .forms
from .forms import RoomForm, UserForm, MyUserCreationForm
# for creating user from default django user
# from django.contrib.auth.models import User
# for splash messages
from django.contrib import messages
# for restrictions
from django.contrib.auth.decorators import login_required
#  for authentications
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm



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
            messages.error(request,"Username or password is incorrect")
    context = {}
    return render(request, 'base/login.html',context)

def signupPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        # print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('homePage')
        else:
            messages.error(request, "An error occurred during registartion ")
            
    context = {'form':form}
    return render(request, 'base/signup.html',context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 
    rooms = Room.objects.filter(Q(topic__name__contains= q) |
                                Q(name__contains = q) |
                                Q(description__contains = q))
    
    forIndRooms = Room.objects.filter(Q(topic__name__contains= q))
    
    # q = request.GET.get('q')  
    # if q:  
    #     rooms = Room.objects.filter(topic__name__icontains=q)
    # else:  
    #     rooms = Room.objects.all()
    # print(rooms)
    roomCount = forIndRooms.count()
    topics = Topic.objects.all()[:5]
    # print(roomCount)
    roomMessages = Message.objects.filter(Q(room__topic__name__contains=q))
    context = {"rooms": rooms, "topics":topics,"roomCount":roomCount, 'roomMessages':roomMessages,'topicCount':topics.count()}
    return render(request, "base/home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    roomMessages = room.message_set.all()
    participants = room.participants.all()
    # rooms = Room.objects.get(id=pk)
    # print(type(rooms))
    room = Room.objects.get(id=pk)
    
    
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk = room.id)
    
    context = {"room": room,'roomMessages':roomMessages, 'participants':participants}
    return render(request, "base/room.html", context)


@login_required(login_url='loginPage')
def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() 
    roomMessages = user.message_set.all()
    topics = Topic.objects.all()
    
    context = {'user':user,'rooms':rooms,'roomMessages':roomMessages,'topics':topics}
    return render(request, 'base/profile.html',context)


@login_required(login_url='loginPage') 
def createRoom(request):
    aboutPage = "Create"
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        print(request.POST)
        topicName = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topicName)
        
        Room.objects.create(
            host= request.user,
            topic = topic,
            name = request.POST.get("name"),
            description = request.POST.get('description')
        )
        return redirect('homePage')
        # request.POST.get('name') # if without ModelForm
    isUpdateRoom = True
    context = {"form": form,"topics":topics,'aboutPage':aboutPage, 'isUpdateRoom':isUpdateRoom}
    return render(request, "base/createRoom.html", context)

@login_required(login_url='loginPage')
def updateRoom(request,pk):
    aboutPage = "Update"
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed to edit this room..!')
    if request.method == 'POST':
        topicName = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topicName)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('homePage')
    context = {'form':form,'topics':topics,'room':room,'aboutPage':aboutPage}
    return render(request,"base/createRoom.html",context)

@login_required(login_url='loginPage')   
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk) 
    if request.user != room.host:
        return HttpResponse('You are not allowed to delete this room..!')
    if request.method == 'POST':
        room.delete()
        return redirect('homePage')
    return render(request,'base/delete.html',{'obj':room})


@login_required(login_url='loginPage')   
def deleteMessage(request,pk):
    try:
        roomMessage = Message.objects.get(id=pk) 
    except:
        messages.error(request, 'Message does not exist')
        return redirect('homePage')
    if request.user != roomMessage.user:
        return HttpResponse('You are not allowed to delete this room..!')
    if request.method == 'POST':
        roomMessage.delete()
        return redirect('homePage')
    return render(request,'base/delete.html',{'obj':roomMessage})


@login_required(login_url='loginPage')   
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method =='POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile',pk=user.id)
    
    
    
    context = {'form':form}
    return render(request,'base/updateUser.html',context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 
    topics = Topic.objects.filter(Q(name__contains=q))
    # print(type(topics))
    count =1
    return render(request,'base/topics.html',{'topics':topics[:5],'count':count})

def activityPage(request):
    roomMessages = Message.objects.all()
    
    return render(request,'base/activity.html',{'roomMessages':roomMessages})