from multiprocessing.connection import Client
from django.shortcuts import render

from api import models

from rest_framework import viewsets
from api.serializer import *
from .models import Client
from rest_framework.permissions import IsAuthenticated

class ClientViews(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # permission_classes =[IsAuthenticated]
