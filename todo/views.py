import datetime
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from rest_framework.views import APIView
from todo.serializers import *
from .models import Person, Todo
from rest_framework.response import Response

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
    
class RegistrationView(View):
    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        Enc_email = make_password(email)
        password = request.POST.get('password')
        Enc_password = make_password(password)
        # this is used to encript the password when it user is registered
        new_person = Person.objects.create(name=name, email=Enc_email, password=Enc_password)
        new_person.save()
        return redirect("login")

class LoginView(APIView):
    def get(self, request):
        try:
            return render(request,'login.html')
        except LoginView.DoesNotExist:
            raise Http404
    def post(self, request):
        serializer = ToDoSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                person = Person.objects.get(email=email)
                if check_password(password, person.password):
                    request.session['email'] = email
                return redirect('todo')
            except Person.DoesNotExist:
                pass

            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['email'] = email
                return redirect('admindash') 
            except User.DoesNotExist:
                pass

            msg = 'Errors: Email or password is invalid'
            return render(request, "login.html", {"msg": msg})

        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })

class TodoView(APIView):
    def get(self, request):
        user_email = request.session.get('email')
        if user_email:
            user_instance = get_object_or_404(Person, email=user_email)
            addtask = Todo.objects.filter(user_id=user_instance.id)
            return render(request, 'todo.html', {'addtask': addtask})
        else:
            return redirect('login')

    def post(self, request):
        serializer = ToDoSerializer(data=request.POST)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                person = Person.objects.get(email=email)
                if check_password(password, person.password):
                    request.session['email'] = email
                    date = datetime.date.today()
                    title = request.POST.get('title')
                    description = request.POST.get('description')
                    logedinUser = get_object_or_404(Person, id=person.id)
                    new_todo = Todo.objects.create(user_id=logedinUser, date=date, title=title, description=description)
                    new_todo.save()
                    return redirect('todo')
            except Person.DoesNotExist:
                pass

            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
 
                    return redirect('admindash') 
            except User.DoesNotExist:
                pass

            msg = 'Errors: Email or password is invalid'
            return render(request, "login.html", {"msg": msg})

        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })
class FinishedView(View):
    def get(self,id):
        todo = Todo.objects.get(id=id)
        todo.completed = True
        todo.status = "completed"
        todo.save()
        return redirect('todo')


class LogoutView(APIView):
    def get(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            
            return redirect('login')
        else:
            return Response(serializer.errors, status=400)

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
