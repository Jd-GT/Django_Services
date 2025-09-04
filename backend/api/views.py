from rest_framework import generics,permissions
from .serializers import ToDoSerializer, ToDoToggleCompleteSerializer
from todo.models import ToDo
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


class TodoList(generics.ListAPIView):
    serializer_class = ToDoSerializer

    def get_queryset(self):
        user = self.request.user
        return ToDo.objects.filter(user=user).order_by('-created')
    
class ToDoListCreate(generics.ListCreateAPIView):
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ToDoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user= self.request.user
        return ToDo.objects.filter(user=user)
    

class ToDoToggleComplete(generics.UpdateAPIView):
    serializer_class = ToDoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.instance.completed = not serializer.instance.completed
        serializer.save()



@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    try:
        data = request.data
        user = User.objects.create_user(
            username=data['username'],
            password=data['password']
        )
        user.save()
        token = Token.objects.create(user=user)
        return JsonResponse({'token': str(token)}, status=201)
    except IntegrityError:
        return JsonResponse(
            {'error': 'username taken. choose another username'},
            status=400
        )



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = request.data
    user = authenticate(
        request,
        username=data['username'],
        password=data['password']
    )
    if user is None:
        return JsonResponse(
            {'error': 'unable to login. check username and password'},
            status=400
        )
    else:
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': str(token)}, status=201)
