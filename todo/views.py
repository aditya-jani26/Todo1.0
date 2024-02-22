import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Person,Todo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth.models import User
# ============================home=====================================
# This is basic page which you can see link

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
            # print(user)

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

        return redirect("login")
    return render(request,'registration.html')

# ==============================todo===================================
@login_required
def todo(request):
    user_email = request.session.get('email')
    if user_email:
        user_instance = get_object_or_404(Person, email=user_email)
        addtask = Todo.objects.filter(user_id=user_instance.id) 
        return render(request,'todo.html',{'addtask':addtask})    
    else:
        return redirect('login')

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
        # print("Title from frontend", logedinUser)
        return redirect('todo')
    return render(request,'todo.html')
# -----------------------------completed-----------------------------------
# here the default value is false

def finished(request,id):
    todo = Todo.objects.get(id=id)
    todo.completed =True

    todo.status = "completed"
    todo.save()

    return redirect('todo')

# -----------------------------logoutuser-----------------------------------
# the cookies will be deleted with

def logout(request):
    try:
        if request.method == 'GET':
            del request.session['email']
            return redirect('login')
    except KeyError:
        return redirect('login') 

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
@login_required
def adminDash(request):
    if request.session['email']:
        users = Person.objects.all()
        return render(request, 'admindashbord.html', {'users': users})
    else:
        return redirect('login')

# --------------------------------------000--------------------------------