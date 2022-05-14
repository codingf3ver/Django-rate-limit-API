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
        serializer = MessageSerializers(all_messages, many=True)
        return Response(serializer.data)
       
    def post(self, request, *args, **kwargs):
        message_data = request.data
        create_message = Message.objects.create(message=message_data['message'], created_at=message_data['created_at'], updated_at=message_data['updated_at'])
        create_message.save()
        serializer = MessageSerializers(create_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       