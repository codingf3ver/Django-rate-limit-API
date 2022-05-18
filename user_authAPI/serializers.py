from nbformat import read
from numpy import source
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message

class userSerializers(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ['id','username','first_name','last_name','email']

class MessageSerializers(serializers.ModelSerializer):
    created_by = userSerializers(read_only=True)
    class Meta:
        model = Message
        fields = ['message_id','message','created_at','updated_at','created_by']


