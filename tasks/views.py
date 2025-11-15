from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Task
from .forms import TaskForm

# Create your views here.


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        "tasks": tasks,
        "show_dates": settings.SHOW_TASK_DATES,
        "show_importance": settings.ENABLE_TASK_IMPORTANCE
    })

@login_required
def tasks_completed(request):
    # Solo mostrar si la característica está habilitada
    if not settings.ENABLE_COMPLETED_TASKS_VIEW:
        return redirect('tasks')
    
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        "tasks": tasks,
        "completed_view": True,
        "show_dates": settings.SHOW_TASK_DATES,
        "show_importance": settings.ENABLE_TASK_IMPORTANCE
    })


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {
            "form": TaskForm,
            "show_importance": settings.ENABLE_TASK_IMPORTANCE
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                "form": TaskForm, 
                "error": "Error creating task.",
                "show_importance": settings.ENABLE_TASK_IMPORTANCE
            })


def home(request):
    return render(request, 'home.html', {
        "product_name": settings.PRODUCT_NAME
    })


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('tasks')
    
    

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task, 
            'form': form,
            'show_complete_button': settings.ENABLE_TASK_COMPLETION,
            'show_importance': settings.ENABLE_TASK_IMPORTANCE,
            'show_dates': settings.SHOW_TASK_DATES
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task, 
                'form': form, 
                'error': 'Error updating task.',
                'show_complete_button': settings.ENABLE_TASK_COMPLETION,
                'show_importance': settings.ENABLE_TASK_IMPORTANCE
            })

@login_required
def complete_task(request, task_id):
    # Solo permitir si la característica está habilitada
    if not settings.ENABLE_TASK_COMPLETION:
        return redirect('tasks')
    
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')