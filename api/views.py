from multiprocessing.connection import Client
from django.shortcuts import render

from api import models

from rest_framework import viewsets
from api.serializer import *
from .models import Client


class ClientViews(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
