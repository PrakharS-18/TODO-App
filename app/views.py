from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app.forms import TODOform, TODO
from django.contrib.auth.decorators import login_required


# Create your views here.

def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOform(data=request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return redirect('home')
        else:
            form = TODOform()
            return render(request, 'index.html', context={'form': form})


@login_required(login_url='login')  # important use for decorater
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOform()
        todos = TODO.objects.filter(user=user).order_by('priority') # sorting acc to priority place minus sign for decen
        return render(request, 'index.html', context={'form': form, 'todos': todos})


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            context = {
                "form": form
            }
            return render(request, 'login.html', context=context)


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        # creating a context variable:- which is basically a data passed to a html file
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)
    else:
        form = UserCreationForm(data=request.POST)
        # creating a context variable:- which is basically a data passed to a html file
        context = {
            "form": form
        }
        if form.is_valid():
            # return HttpResponse("Form is Invalid")
            user = form.save()
            if user is not None:
                return redirect('home')
        else:
            return render(request, 'signup.html', context=context)


def signout(request):
    logout(request)
    return redirect('login')


def delete_todo(request, id):
    TODO.objects.get(pk = id).delete()
    return redirect('home')


def status_todo(request, id, status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')

