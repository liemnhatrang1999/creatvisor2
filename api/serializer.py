from rest_framework import serializers,exceptions
from .models import *
from django.contrib.auth import get_user_model,authenticate
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User= get_user_model()
from rest_framework.serializers import ModelSerializer
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from rest_framework.validators import UniqueValidator
from allauth.account.adapter import get_adapter
try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

from django.db import transaction
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from dj_rest_auth.serializers import JWTSerializer
from rest_auth  import serializers as auth_serializers

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken


class UserSerializer(FlexFieldsModelSerializer):
    class Meta :
        model = User
        fields = ('prenom','nom','email','phone','is_active','is_consultant')

class Thematique_metierSerializer(FlexFieldsModelSerializer):
    class Meta :
        model = Thematique_metier
        fields = ('id','nom')

class Info_entrepreneurSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Info_entrepreneur
        fields = ('photo','valeur_humaine','secteur','problematique','project','user')
        expandable_fields = { 
            'user' : (UserSerializer,{'many' : True}),
        }

class Info_consultantSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Info_consultant
        fields = ('photo','valeur_humaine','experiences','competances','user')
        expandable_fields = { 
            'user' : (UserSerializer,{'many' : True}),
        }        
class AtelierSerializer(FlexFieldsModelSerializer):
    class Meta :
        model = Atelier
        fields = ('id','nom','pre_requis','participants','thematique_metier','creator','expires_date')
        expandable_fields = { 
            'participants' : (Info_entrepreneurSerializer,{'many' : True}),
            'thematique_metier' :(Thematique_metierSerializer,{'many' : True}),
            'creator' :(Info_consultantSerializer,{'many' : True}),
        }
    def save(self, *args, **kwargs):
        #if test_result is less than 80 execute this
        # counter  = self.participants.count()
        counter = len(self.validated_data['participants'])
        print(counter)
        t = []
        for telephone in self.validated_data['participants'] :
            t.append(telephone.user.get().phone)
        print(t)
        account_sid = 'ACe55b0a3feed28b2eb15d65afb854db83'
        auth_token = 'e2206a2e55fb538bd25f4901dbfd7709'
        client = Client(account_sid, auth_token)
        # for telephone in t:
            
        #     try:
        #         print(telephone)
        #         validation_request = client.validation_requests \
        #                                 .create(
        #                                         friendly_name=f'phone{telephone}',
        #                                         phone_number=telephone
        #                                     )
        #         print(validation_request.friendly_name)
        #     except Exception as e:
        #         print(e)
                
        if counter == 4 :
            #twilio code
            for telephone in t:
                
                message = client.messages.create(
                                            body=f'Bonjour , votre atelier est complet',
                                            from_='+15139934888',
                                            to=telephone)

                print(message.sid)
        return super().save(*args, **kwargs)

class AvisSerializer(FlexFieldsModelSerializer):
    class Meta  :
        model = Avis
        fields =('user','ponctualite','qualite','respect','atelier','commentaire')
        expandable_fields = { 
            'user' : (UserSerializer,{'many' : True}),
            'atelier' :(AtelierSerializer,{'many' : True}),
        }

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['nom'] = user.nom
        token['prenom'] = user.prenom
        token['is_consultant'] = user.is_consultant
        return token


class MyRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only = True,required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User

        fields = ('prenom','nom','email','phone','password','password2','is_consultant')
        extra_kwargs = {
            'prenom': {'required': True},
            'nom': {'required': True},
            'phone': {'required': True},
        }
  
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    ("A user is already registered with this e-mail address."))
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs
    def get_cleaned_data(self):
        return {
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'prenom': self.validated_data.get('prenom', ''),
            'nom': self.validated_data.get('nom', ''),
            'phone': self.validated_data.get('phone', ''),
            'is_consultant': self.validated_data.get('is_consultant', ''),
        }
    def custom_signup(self, request, user):
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


    @transaction.atomic
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.prenom = self.cleaned_data['prenom'] 
        user.nom = self.cleaned_data['nom'] 
        user.phone = self.cleaned_data['phone'] 
        user.is_consultant = self.cleaned_data['is_consultant']
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class MyLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['email','password']
    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = authenticate(self.context.get('request'), email=email, password=password)
            if user is None:
                msg = _('Email or password is incorrect')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:

                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError({"error":"Email is not verified"})

        attrs['user'] = user
        
        return attrs


