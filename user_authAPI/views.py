from email import message
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

from django.http import Http404
# Create your views here.

def home(request):
    return HttpResponse("Hello, world. You're at the API tesing home")

class userviewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers

class MessageView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request,*args, **kwargs):
        try:
            message = Message.objects.all()
            message_serializer = MessageSerializers(message, many=True)

            json_data = json.dumps(message_serializer.data,indent=4)
            with open('results.json', 'w') as f:
                f.write(json_data)
            return Response(message_serializer.data, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            raise Http404
        
    def post(self, request, *args, **kwargs):

        message_data = request.data
        current_user = request.user

        create_message = Message.objects.create(message=message_data['message'],created_by_id=current_user.id)
        create_message.save()
        
        data={ 
            'message': 'success',
            'status': status.HTTP_201_CREATED
        }
        with open('messages.json', 'w') as outfile:
            json.dump(data, outfile)

        return Response(data ,status=status.HTTP_201_CREATED)
    
    def put(self, request, *args, **kwargs):
        message_data = request.data
        try:
            message_id = message_data['id']
            Message.objects.filter(id=message_id).update(message=message_data['message'],updated_at=message_data['updated_at'])
            data={ 
                'message': 'message updated',
                'status': status.HTTP_201_CREATED
            }
            return Response(data ,status=status.HTTP_201_CREATED)
        except Message.DoesNotExist:
            raise Http404

    def delete(self, request, *args, **kwargs):
        message_data = request.data

        try:
            message_id = message_data['id']
            Message.objects.filter(id=message_id).delete()
            data={ 
                'message': 'user deleted',
                'status': status.HTTP_201_CREATED
            }
            return Response(data ,status=status.HTTP_201_CREATED)

        except Message.DoesNotExist:
            raise Http404
