import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ToDoSerializer
from .models import Person, Todo
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import status

# ============================home=====================================
# This is basic page which you can see link

def home(request):
    return render(request, 'home.html')

# ------------------------------login----------------------------------
# this is login function in this we have used session to login 
def login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        Enc_password = make_password(password)

        user = User.objects.get(username="admin")

        if Person.objects.filter(email=email).exists() and check_password(password, Enc_password):  
            request.session['email'] = email
            return redirect('todo_list')
        
        elif User.objects.filter(email=user.email).exists() and check_password(password, user.password):
            request.session['email'] = email
            return redirect('admindash')
        
        else:
            msg = 'Errors:Email or password is invalid' 
            return render(request, "login.html", {"msg": msg})
    return render(request, 'login.html')

# ---------------------------registration-------------------------------------
# this is when new user come for the first time can want to register and create a new account
def registration(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        Enc_email = make_password(email)
        password = request.POST.get('password')
        Enc_password = make_password(password)
        new_person = Person.objects.create(name=name, email=Enc_email, password=Enc_password)
        new_person.save()

        return redirect("login")
    return render(request, 'registration.html')

# ==============================todo===================================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.filter(user=request.user)
        serializer = ToDoSerializer(todos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo_detail(request, pk):
    try:
        todo = Todo.objects.get(pk=pk, user=request.user)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ToDoSerializer(todo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ToDoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ------------------------------add----------------------------------

def add(request):
    if request.method == 'POST':
        date = datetime.date.today()
        title = request.POST.get('title')
        description = request.POST.get('description')
        obj = Person.objects.get(email=request.session['email'])
        logedinUser = get_object_or_404(Person, id=obj.id)
 
        new_todo = Todo.objects.create(user_id=logedinUser, date=date, title=title, description=description)
        new_todo.save()
        return redirect('todo')
    return render(request, 'todo.html')

# -----------------------------completed-----------------------------------
# here the default value is false

def finished(id):
    todo = Todo.objects.get(id=id)
    todo.completed = True
    todo.status = "completed"
    todo.save()

    return redirect('todo')

# -----------------------------logoutuser-----------------------------------
# the cookies will be deleted with

def logout(request):
    del request.session['email']
    return redirect('login')

# ---------------------------delete-------------------------------------
# this is used to delete the task from the database

def delete(request, id):
    todo = Todo.objects.get(id=id)
    todo.delete()
    return redirect('todo')

# -----------------------------display-----------------------------------
@login_required
# This is used for admin dashboard only (see this on admindashbors.Html)
def display(request, id):
    user_email = request.session.get('email')
    if user_email:
        todo = Todo.objects.filter(user_id=id)
        return render(request, 'display.html', {'todo': todo})
    else:
        return redirect('login')
   
# this Dispaly. Html file j 
# --------------------------------adminDash--------------------------------
# This is used for Showing all user information and task
def admindash(request):
    if request.session['email']:
        users = Person.objects.all()
        return render(request, 'admindashbord.html', {'users': users})
    else:
        return redirect('login')
