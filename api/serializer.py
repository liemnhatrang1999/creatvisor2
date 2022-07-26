
from itertools import count
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User= get_user_model()
from rest_framework.serializers import ModelSerializer
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin

# class ClientSerializer(serializers.ModelSerializer) :
#     class Meta : 
#         model = Client
#         fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ('prenom','nom','email','phone','is_active')

class Thematique_metierSerializer(FlexFieldsModelSerializer):
    class Meta :
        model = Thematique_metier
        fields = ('id','nom')

class AtelierSerializer(FlexFieldsModelSerializer):
    
    class Meta :
        model = Atelier
        fields = ('id','nbparticipants','nom','pre_requis','participants','thematique_metier')
        expandable_fields = { 
            'participants' : (UserSerializer,{'many' : True}),
            'thematique_metier' :(Thematique_metierSerializer,{'many' : True})
        }
            # dict(participant = serializers.SerializerMethodField)
    # def to_representation(self, instance):
    #     data = super(AtelierSerializer, self).to_representation(instance)
        
    #     data['participants']
    #     return data
    
    # def get_participants(self, atelier):
    #     return count(atelier['participants'])
class Info_entrepreneurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info_entrepreneur
        fields = ('photo','valeur_humaine','secteur','problematique','project_professionnel')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['nom'] = user.nom
        token['prenom'] = user.prenom
        token['is_consultant'] = user.is_consultant
        return token