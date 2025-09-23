from django.urls import path
from . import views


urlpatterns = [
    
    path("login/", views.loginPage, name="loginPage"),
    path("sign-up/", views.signupPage, name="signupPage"),
    path("logout/", views.logoutUser, name="logoutUser"),
    
    
    path("", views.home, name="homePage"),
    path("room/<str:pk>/", views.room, name="room"),
    path("profile/<str:pk>", views.userProfile, name="userProfile"),
    
    
    
    path("create-room/", views.createRoom, name="createRoom"),
    path("update-room/<str:pk>/", views.updateRoom, name="updateRoom"),
    path("delete-room/<str:pk>/", views.deleteRoom, name="deleteRoom"),
    path("delete-message/<str:pk>/", views.deleteMessage, name="deleteMessage"),
    
    
    path("update-user/", views.updateUser, name="updateUser"),
    
    path("topics/", views.topicsPage, name="topicsPage"),
    path("activities/", views.activityPage, name="activityPage"),
    
]
