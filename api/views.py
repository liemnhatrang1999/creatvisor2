import email
from urllib import response
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework.decorators import action
from django.shortcuts import render
from rest_framework import generics

from rest_framework.response import Response
from api import models
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from api.serializer import *
# from .models import Client
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK )



# class ClientViews(viewsets.ModelViewSet):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
#     # permission_classes =[IsAuthenticated]


# @csrf_exempt
# @api_view(["POST"])
# @permission_classes((AllowAny,))
# def login(request):
#     emailClient = request.data.get("emailClient")
#     passwordClient = request.data.get("passwordClient")
#     if emailClient is None or passwordClient is None:
#         return Response({'error': 'Please provide both username and password'},
#                         status=HTTP_400_BAD_REQUEST)
#     user = authenticate(email=emailClient, password=passwordClient)
#     if not user:
#         return Response({'error': 'Invalid Credentials'},
#                         status=HTTP_404_NOT_FOUND)
#     token, _ = Token.objects.get_or_create(emailClient=emailClient)
#     return Response({'token': token.key},
#                     status=HTTP_200_OK)

# class MyAccountManager(BaseUserManager):
#     def create_user(self, nomClient=None, prenomClient=None, emailClient=None, mobileClient =None,passwordClient=None
#                     ):
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             Email_Address=self.normalize_email(email),
#             name=self.normalize_email(email),
#             Date_of_Birth=birthday,
#             zipcode=zipcode,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

from rest_framework.views import APIView
from rest_framework import permissions,status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()
from .serializer import UserSerializer


class RegisterView(APIView):
    permission_classes =[permissions.AllowAny]
    def post(self,request):
        try :
            data = request.data
            prenom=data['prenom']
            nom = data['nom']
            phone = data['phone']
            email = data['email']
            email = email.lower()
            password = data['password']
            
            # is_consultant = data['is_consultant']

            # if is_consultant == 'True':
            #     is_consultant =True
            
            # else :
            #     is_consultant = False
            
        # if password == re_password :
            if not User.objects.filter(email=email).exists():
                # if is_consultant == True :
                    # User.objects.create_consultant(prenom=prenom,nom=nom,phone=phone,email=email,password=password)
                    # return Response({'reussi' :'oui'},status=status.HTTP_201_CREATED)

                # else :
                    User.objects.create_user(prenom=prenom,nom=nom,phone=phone,email=email,password=password)
                    return Response({'reussi' :'oui'},status=status.HTTP_201_CREATED)
            else:
                return Response({'error':'déjà utilisé'},status=status.HTTP_400_BAD_REQUEST)
        except :
            return Response({"erreur" : "échec "},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset,many=True)
        return Response(serializer.data)

class RetrieveView(APIView):
    def get(self,request):
        try :
            user = request.user
            user = UserSerializer(user)
            return Response({'user':user.data},status=status.HTTP_200_OK)

        except:
            Response({"error" : "something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)