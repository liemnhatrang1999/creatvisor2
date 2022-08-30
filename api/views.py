from ast import keyword
from asyncio import mixins
import email
from email import message
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import JsonResponse
from rest_framework.decorators import action
from django.shortcuts import render
from rest_framework import generics
import django_filters.rest_framework
from rest_framework.response import Response
from api import models
from rest_framework import viewsets,filters
from api.serializer import *
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

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import *
from django.core.mail import EmailMessage
from backend.settings import EMAIL_HOST_USER
from rest_flex_fields.views import FlexFieldsModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.views import VerifyEmailView,ConfirmEmailView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from rest_framework import permissions,status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()
from .serializer import UserSerializer
from rest_framework.compat import coreapi, coreschema, distinct
import operator
from functools import reduce


class DynamicSearchFilter(filters.SearchFilter):
     def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)
        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in search_fields
        ]

        base = queryset
        conditions = []
        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]

            conditions.append(reduce(operator.or_, queries))
        queryset = queryset.filter(reduce(operator.or_, conditions))

        if self.must_call_distinct(queryset, search_fields):
            # Filtering against a many-to-many field requires us to
            # call queryset.distinct() in order to avoid duplicate items
            # in the resulting queryset.
            # We try to avoid this if possible, for performance reasons.
            queryset = distinct(queryset, base)
        return queryset

class RegisterView(FlexFieldsModelViewSet):
    permission_classes =[permissions.AllowAny]
    def post(self,request):
        try :
            data = request.data
            prenom = data['prenom']
            nom = data['nom']
            phone = data['phone']
            email = data['email']
            email = email.lower()
            password = data['password']
            is_consultant = data['is_consultant']
            
        # if password == re_password :
            if not User.objects.filter(email=email).exists():

                if is_consultant == True :
                    thematique =data['thematique']
                    experiences = data['experiences']
                    competances = data['competances']
                    # reseau = data['reseau']
                    # linkedin = data['linkedin'] 
                    user = User.objects.create_consultant(
                        prenom=prenom,
                        nom=nom,
                        phone=phone,
                        email=email,
                        password=password,
                        )
                    user.is_active = False
                    user.save()
                    # info_consultant = Info_consultant.objects.create(
                    #     thematique=thematique,
                    #     experiences=experiences,
                    #     competances=competances,
                    #     # reseau=reseau,
                    #     # linkedin=linkedin,
                    #     id_consultant=user)
                    # info_consultant.save()
                    
                    
                else :
                
                    user = User.objects.create_user(prenom=prenom,nom=nom,phone=phone,email=email,password=password)
                    user.is_active = False
                    user.save()
                    # info_entrepreneur = Info_entrepreneur.objects.create()
                    # info_entrepreneur.save()


                current_site = get_current_site(request)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                mail_subject = 'Activate your blog account.'
                message = f"Hi , Please click on the link to confirm your registration, http://{current_site.domain}/activate/{uid}/{token}/"
                # message = render_to_string('acc_active_email.html', {
                #     'user': User,
                #     'domain': current_site.domain,
                #     'uid':urlsafe_base64_encode(force_bytes(User.pk)),
                #     'token':account_activation_token.make_token(User),
                # })
                
                email1 = EmailMessage(
                            mail_subject, message, settings.EMAIL_HOST_USER,[email]
                )
                email1.send()
                return Response({'reussi' :'oui'},status=status.HTTP_201_CREATED)    
            else:
                return Response({'error':'déjà utilisé'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"erreur" : "echec"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def activate(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64).decode())
            # uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
   
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            
            # return redirect('home')
            return JsonResponse({'reussi' :'oui'},status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(
                {'error' :'something went wrong!'},
                status=status.HTTP_201_CREATED
            )

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

class AtelierView(FlexFieldsModelViewSet):
    queryset = Atelier.objects.all()
    serializer_class = AtelierSerializer
    permit_list_expands =['participants','thematique_metier','participants.user','creator','creator.competances','creator.user']
    filter_backends = [DynamicSearchFilter,]
    search_fields = ['thematique_metier__nom','creator__competances__nom',"participants__user__id"]
    filterset_fields =('thematique_metier')
    permission_classes=[AllowAny]

# class AtelierCreatorView(FlexFieldsModelViewSet):
#     queryset = Atelier.objects.all()
#     serializer_class = AtelierSerializer
#     permit_list_expands =['participants','thematique_metier','participants.user','creator','creator.competances','creator.user']
#     filter_backends = [DynamicSearchFilter,]
#     search_fields = ['thematique_metier__nom','creator__competances__nom',"creator__id"]
#     filterset_fields =('thematique_metier')
#     permission_classes=[AllowAny]


class DetailAtelier(APIView):
    def get(self,request,pk):
        atelier = Atelier.objects.get(pk=pk)
        serializer = AtelierSerializer(atelier)
        return Response(serializer.data)
        
class Info_entrepreneurView(FlexFieldsModelViewSet):
    queryset = Info_entrepreneur.objects.all()
    serializer_class = Info_entrepreneurSerializer
    permit_list_expands =['user']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # search_fields = ['user__id']
    filterset_fields =('user',)
    permission_classes =[AllowAny]
    
class Info_consultantView(FlexFieldsModelViewSet):
    queryset = Info_consultant.objects.all()
    serializer_class = Info_consultantSerializer
    permit_list_expands =['user','competances']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # search_fields = ['user__nom','competances__nom']
    filterset_fields =('user','competances')
    permission_classes =[AllowAny]
    
class AvisView(FlexFieldsModelViewSet):
    queryset = Avis.objects.all()
    serializer_class = AvisSerializer
    permit_list_expands =['user','atelier','atelier.creator.user','atelier.creator','atelier.creator.user']
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__nom','atelier__nom','atelier__id']
    filterset_fields =('user','atelier','atelier.creator')
    permission_classes =[AllowAny]

class ThematiqueView(FlexFieldsModelViewSet):
    queryset = Thematique_metier.objects.all()
    serializer_class = Thematique_metierSerializer
    permission_classes =[AllowAny]

class GoogleLogin(SocialLoginView): 
    adapter_class = GoogleOAuth2Adapter
    # callback_url = 
    client_class = OAuth2Client

class FacebookLogin(SocialLoginView): 
    adapter_class = FacebookOAuth2Adapter
    clienlt_class = OAuth2Client

# class VerifyEmailView(APIView, ConfirmEmailView):
#     # ...

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.kwargs['key'] = serializer.validated_data['key']
#         confirmation = self.get_object()
#         confirmation.confirm(self.request)
#         return Response({'detail': _('ok')}, status=status.HTTP_200_OK)

class BlacklistRefreshView(APIView):
    def post(self, request) :
        token = RefreshToken(request.data.get('refresh_token'))
        token.blacklist()
        return Response("Success")

class PartenaireView(FlexFieldsModelViewSet):
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireSerializer
    permit_list_expands =['thematique_metier']
    filter_backends = [DynamicSearchFilter,]
    search_fields = ['thematique_metier__nom']
    filterset_fields =('thematique_metier',)
    permission_classes=[AllowAny]

class UserDetailApiView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class=UserSerializer
    def get_object(self):
        return self.request.user

class FormationView(FlexFieldsModelViewSet):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer
    # permit_list_expands =['consultant']
    # filter_backends = [DynamicSearchFilter,]
    # search_fields = ['consultant__id']
    # filterset_fields =('constultant',)
    permission_classes=[AllowAny]

class CertificationView(FlexFieldsModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    # permit_list_expands =['consultant']
    # filter_backends = [DynamicSearchFilter,]
    # search_fields = ['consultant__id']
    # filterset_fields =('constultant',)
    permission_classes=[AllowAny]

class ExpView(FlexFieldsModelViewSet):
    queryset = Exp.objects.all()
    serializer_class = ExpSerializer
    # permit_list_expands =['consultant']
    # filter_backends = [DynamicSearchFilter,]
    # search_fields = ['consultant__id']
    # filterset_fields =('constultant',)
    permission_classes=[AllowAny]

