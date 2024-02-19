import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Person,Todo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password 
from django.contrib.auth.models import User
# ============================home=====================================
# This is basic page which you can see link
@login_required
def home(request):
    return render(request,'home.html')

# ------------------------------login----------------------------------
# this is login function in this we have used session to login 
def login(request):

        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password') 

            # user = request.user

            user = user = User.objects.get(username = "admin")
            print(user)

            if Person.objects.filter(email=email, password=password).exists():  
                request.session['email'] = email
                return redirect('todo')
            elif User.objects.filter(email=user.email).exists() and check_password(password, user.password):
                request.session['email'] = email
                return redirect('adminDash')
            else:
                return HttpResponse("Either email or password is incorrect.")
        return render(request, 'login.html')

# ---------------------------registration-------------------------------------
# this is when new user come for the first time can want to register and create a new account
def registration(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        newPerson = Person(name=name, email=email, password=password)
        newPerson.save()

        request.session['email'] = email
        return redirect("login")
    return render(request,'registration.html')

# ==============================todo===================================

def todo(request):
    addtask = Todo.objects.all()
    return render(request,'todo.html',{'addtask':addtask})
# ------------------------------add----------------------------------

@login_required
def add(request):
    if request.method == 'POST':
        date = datetime.date.today()
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        obj= Person.objects.get(email=request.session['email'])
        logedinUser = get_object_or_404(Person,id=obj.id)
 
        new_todo = Todo.objects.create(user_id=logedinUser, date=date, title=title, description=description)
        new_todo.save()
        print("Title from frontend", title)
        return redirect('todo')
    return render(request,'todo.html')
# -----------------------------completed-----------------------------------
# here the default value is false

def completed(request,id):
    todo = Todo.objects.get(id=id)


    if todo.completed == True:
        todo.status = "completed"

    Todo.objects.filter(status=todo.status)
    todo.save()

    return redirect('home')

# -----------------------------logoutuser-----------------------------------
# the cookies will be deleted with

def logout(request):
    del request.session['email']
    return render(request, 'login.html')

# ---------------------------delete-------------------------------------
# this is used to delete the task from the database

def delete(request,id):
    todo = Todo.objects.get(id=id)
    todo.delete()
    return redirect('todo')

# -----------------------------display-----------------------------------

# This is used for admin dashboard only (see this on admindashbors.Html)
def display(request,id):
    
    todo=Todo.objects.filter(user_id=id)

    return render(request,'display.html',{'todo':todo})
# this Dispaly. Html file j 
# --------------------------------adminDash--------------------------------
# This is used for Showing all user information and task
def adminDash(request):

    users = Person.objects.all()
    return render(request, 'admindashbord.html', {'users': users})
# --------------------------------------000--------------------------------