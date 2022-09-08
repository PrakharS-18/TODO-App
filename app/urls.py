from django.contrib import admin
from django.urls import path
from .views import home, signup, login, add_todo, signout, delete_todo, status_todo

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', signout, name='logout'),
    path('signup/', signup, name='signup'),
    path('add-todo/', add_todo, name='add-todo'),
    path('delete-todo/<int:id>', delete_todo, name='delete-todo'),
    path('change-status/<int:id>/<str:status>', status_todo)
]


