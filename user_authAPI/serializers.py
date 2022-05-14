from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message

class userSerializers(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = '__all__'

class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

