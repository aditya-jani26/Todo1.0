import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Person,Todo
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.hashers import check_password 
# ============================home=====================================

def home(request):
    return render(request,'home.html')

# ------------------------------login----------------------------------

def login(request):

        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password') 
            if Person.objects.filter(email=email, password=password).exists():  
                request.session['email'] = email
                return redirect('todo')
            elif Person.objects.filter(email=Person.email).exists() and check_password(password, request.Person.password):
                request.session['email'] = email
                return redirect('adminDash')
            else:
                return HttpResponse("Either email or password is incorrect.")
        return render(request, 'login.html')

# ---------------------------registration-------------------------------------

def registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        newPerson = Person(name=name, email=email, password=password)
        newPerson.save()
        return redirect("login")
    return render(request,'registration.html')

# ==============================todo===================================

def todo(request):
    addtask = Todo.objects.all()
    # count = 0
    # for i in addtask:
    #     count += 1
    #     print(i.id)
    #     i.id = count
    return render(request,'todo.html',{'addtask':addtask})
# ------------------------------add----------------------------------

def add(request):
    if request.method == 'POST':
        date = datetime.date.today()
        title = request.POST.get('title')
        description = request.POST.get('description')
 
        new_todo = Todo.objects.create(date=date, title=title, description=description)
        new_todo.save()
        print("Title from frontend", title)
        return redirect('todo')
    return render(request,'todo.html')
# -----------------------------completed-----------------------------------

def completed(request,id):
    todo = Todo.objects.get(id=id)


    if todo.completed == True:
        todo.status = "completed"

    Todo.objects.filter(status=todo.status)
    todo.save()

    return redirect('home')

# -----------------------------logoutuser-----------------------------------

def logoutuser(request):
    return redirect('login.html')

# ---------------------------delete-------------------------------------
# this is used to delete the task from the database

def delete(request,id):
    todo = Todo.objects.get(id=id)
    todo.delete()
    return redirect('todo')

# -----------------------------display-----------------------------------

# this is used to show data which is in database
def display(request,id):
    
    todo=Todo.objects.filter
    print("Display", sum(todo.id for t in todo))
    return render(request,'todo.html',{'todo':Todo})
# --------------------------------adminDash--------------------------------
def adminDash(request):

    todo = Todo.objects.all()
    return render(request, 'adminDash.html', {'users': Todo})
# --------------------------------------000--------------------------------