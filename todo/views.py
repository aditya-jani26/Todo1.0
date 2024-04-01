import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Person, Todo


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        Enc_password = make_password(password)

        try:
            user = User.objects.get(username="admin")
        except User.DoesNotExist:
            user = None

        if Person.objects.filter(email=email).exists() and check_password(password, Enc_password):
            request.session['email'] = email
            return redirect('todo')
        elif user and User.objects.filter(email=user.email).exists() and check_password(password, user.password):
            request.session['email'] = email
            return redirect('admindash')
        else:
            msg = 'Errors: Email or password is invalid'
            return render(request, "login.html", {"msg": msg})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        Enc_email = make_password(email)
        password = request.POST.get('password')
        Enc_password = make_password(password)
        new_person = Person.objects.create(name=name, email=Enc_email, password=Enc_password)
        new_person.save()
        return redirect("login")


class TodoView(View):
    def get(self, request):
        user_email = request.session.get('email')
        if user_email:
            user_instance = get_object_or_404(Person, email=user_email)
            addtask = Todo.objects.filter(user_id=user_instance.id)
            return render(request, 'todo.html', {'addtask': addtask})
        else:
            return redirect('login')

    def post(self, request):
        if request.method == 'POST':
            date = datetime.date.today()
            title = request.POST.get('title')
            description = request.POST.get('description')
            obj = Person.objects.get(email=request.session['email'])
            logedinUser = get_object_or_404(Person, id=obj.id)
            new_todo = Todo.objects.create(user_id=logedinUser, date=date, title=title, description=description)
            new_todo.save()
            return redirect('todo')


class FinishedView(View):
    def get(self, request, id):
        todo = Todo.objects.get(id=id)
        todo.completed = True
        todo.status = "completed"
        todo.save()
        return redirect('todo')


class LogoutView(View):
    def get(self, request):
        del request.session['email']
        return redirect('login')


class DeleteView(View):
    def get(self, request, id):
        todo = Todo.objects.get(id=id)
        todo.delete()
        return redirect('todo')


class DisplayView(View):
    @login_required
    def get(self, request, id):
        user_email = request.session.get('email')
        if user_email:
            todo = Todo.objects.filter(user_id=id)
            return render(request, 'display.html', {'todo': todo})
        else:
            return redirect('login')


class AdminDashView(View):
    def get(self, request):
        if request.session['email']:
            users = Person.objects.all()
            return render(request, 'admindashbord.html', {'users': users})
        else:
            return redirect('login')
