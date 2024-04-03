import datetime
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken



class RegistrationView(APIView):
    def post(self, request):

        name = request.data.get('name')
        email = request.data.get('email')
        password = make_password(request.data.get('password'))

        if not name or not email or not password:
            return Response({'error': 'Please provide name, email, and password'}, status=status.HTTP_400_BAD_REQUEST)

        if Person.objects.filter(name=name).exists():
            return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        if Person.objects.filter(email=email).exists():
            return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

        user = Person.objects.create(name=name, email=email, password=password)
        if user:
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        

        email = request.data.get('email')
        print("Email",email)
        password =request.data.get('password')

        try:
            person = Person.objects.get(email=email)
            if check_password(password, person.password):
                request.session['email'] = email
                refresh = RefreshToken.for_user(person)
                return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        except Person.DoesNotExist:
            pass
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session['email'] = email
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
        except User.DoesNotExist:
            pass

        msg = 'Errors: Email or password is invalid'
        return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)


class TodoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_email = request.session.get('email')
        if user_email:
            user_instance = get_object_or_404(Person, email=user_email)
            addtask = Todo.objects.filter(user_id=user_instance.id)
            serializer = ToDoSerializer(addtask, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                person = Person.objects.get(email=email)
                if check_password(password, person.password):
                    request.session['email'] = email
                    date = datetime.date.today()
                    title = request.data.get('title')
                    description = request.data.get('description')
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
            return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def finished_view(id):
    try:
        todo = Todo.objects.get(id=id)
        todo.completed = True
        todo.status = "completed"
        todo.save()
        return redirect('todo')
    except Todo.DoesNotExist:
        raise Http404("Todo does not exist")


class LogoutView(APIView):
    def get(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            del request.session['email']
            return redirect('login')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_view(id):
    try:
        todo = Todo.objects.get(id=id)
        todo.delete()
        return redirect('todo')
    except Todo.DoesNotExist:
        raise Http404("Todo does not exist")


@api_view(['GET'])

@permission_classes([IsAuthenticated])
def display_view(request, id):
    user_email = request.session.get('email')
    if user_email:
        todo = Todo.objects.filter(user_id=id)
        serializer = ToDoSerializer(todo, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def admindash_view(request):
    if request.session.get('email'):
        users = Person.objects.all()
        return Response({'users': users})
    else:
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
