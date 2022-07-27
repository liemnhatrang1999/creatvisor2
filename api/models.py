from ast import Pass
from cgitb import text
import email
from pyexpat import model
import site
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager


# class Client(models.Model):
#     nomClient = models.CharField(max_length=240)
#     prenomClient = models.CharField(max_length=240)
#     emailClient = models.EmailField()
#     mobileClient = models.CharField(max_length=20)
#     passwordClient = models.CharField(max_length=240)
#     inscriptionClient = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.nomClient

class UserAccountManager(BaseUserManager):
    def create_user(self, email, prenom,nom,phone, password = None):
        if not email :
            raise ValueError('need email')
        email = self.normalize_email(email)
        email = email.lower()
        
        user = self.model(email = email,prenom = prenom,phone=phone,nom=nom,)
        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_consultant(self,phone, email , prenom,nom ,password = None):
        user = self.create_user(email,prenom,nom,phone,password)
        user.is_consultant = True
        
        user.save(using =self._db)
        return user


    def create_superuser(self, email , prenom ,nom,phone,password = None):
        user = self.create_user(email,prenom,nom,phone,password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        
        user.save(using =self._db)
        return user



# AUTH_PROVIDERS = {'facebook':'facebook','email':'email','google':'google'}




class UserAccount(AbstractBaseUser,PermissionsMixin): 
    email = models.EmailField(max_length=255,unique=True)
    prenom = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    # auth_provider = models.CharField(max_length=255,blank=False,null=False,default=AUTH_PROVIDERS.get('email'))
    # info_entrepreneur = models.ManyToManyField(Info_entrepreneur,blank=True, related_name="info_entrepreneur")
    # info_consultant = models.ManyToManyField(Info_consultant,blank=True, related_name="infor_consultant")

    is_active = models.BooleanField(default=False)
    is_staff   =models.BooleanField(default=False)
    is_consultant  =models.BooleanField(default=False)
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['prenom','nom','phone']    


class Thematique_metier(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self) :
        return self.nom

# class CustomDateTimeField(models.DateTimeField):
#     def value_to_string(self, obj):
#         val = self.value_from_object(obj)
#         if val:
#             val.replace(microsecond=0)
#             return val.isoformat()
#         return ''
class Info_entrepreneur(models.Model):
    photo = models.ImageField( upload_to='media', height_field=None, width_field=None, max_length=None)
    valeur_humaine = models.TextField()
    secteur = models.CharField(max_length=255)
    problematique = models.TextField()
    project = models.TextField(blank=True)
    user = models.ManyToManyField(UserAccount, related_name="info_entrepreneur")

    
    def __str__(self) :
        L=[]
        user= self.user.all()
        for p in user:
            L.append(p)
        B = f"{L[0]}"
        B = B.split(":")
        
        return B[0]
class Atelier(models.Model):
    nbparticipants = models.IntegerField(default=0)
    nom = models.CharField(max_length=255)
    pre_requis = models.TextField(max_length=10000,default="")
    thematique_metier = models.ManyToManyField(Thematique_metier,related_name='atelier',default=None)
    participants = models.ManyToManyField(Info_entrepreneur,related_name="atelier",blank=True)
    
    # date = models.DateTimeField(auto_now=False, auto_now_add=False, )



class Info_consultant(models.Model):
    
    photo = models.ImageField( upload_to='media', height_field=None, width_field=None, max_length=None)
    thematique = models.TextField()
    experiences = models.IntegerField()
    competances = models.TextField()
    valeur_humaine = models.TextField()
    user = models.OneToOneField(UserAccount, related_name="info_consultant",on_delete=models.CASCADE)
# reseau = models.URLField(max_length=200)
    # linkedin = models.URLField(max_length=200)