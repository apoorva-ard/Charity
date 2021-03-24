from rest_framework import serializers 
from . models import *

class CausePostSerializer(serializers.Serializer): 
    id = serializers.IntegerField()
    accept = serializers.BooleanField()

class UserPostSerializer(serializers.Serializer): 
    uname = serializers.CharField()
    pwd = serializers.CharField()

class ContactSerializer(serializers.Serializer): 
    id = serializers.IntegerField()