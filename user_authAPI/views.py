import json
from textwrap import indent
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import userSerializers , MessageSerializers
from .models import Message
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
# Create your views here.

def home(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class userviewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers

class MessageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

    def get(self, request,*args, **kwargs):
        all_messages = Message.objects.all()
        message_serializer = MessageSerializers(data = all_messages, many=True)
        message_serializer.is_valid()
        current_user = request.user
       
        data = {
            'user_id': current_user.id,
            'messages': message_serializer.data,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'email': current_user.email,
            }
        json_data = json.dumps(data,indent=4)
        with open('results.json', 'w') as f:
            f.write(json_data)
        return Response(data , status=status.HTTP_200_OK)
       
    def post(self, request, *args, **kwargs):
        message_data = request.data
        create_message = Message.objects.create(message=message_data['message'], created_at=message_data['created_at'], updated_at=message_data['updated_at'])
        create_message.save()
        serializer = MessageSerializers(create_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

       
