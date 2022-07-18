from ast import Pass
import email
from pyexpat import model
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
    def create_user(self, email, prenom,nom, password = None):
        if not email :
            raise ValueError('need email')
        email = self.normalize_email(email)
        email = email.lower()
        
        user = self.model(email = email,prenom = prenom,nom=nom)
        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_consultant(self, email , prenom,nom ,password = None):
        user = self.create_user(email,prenom,nom,password)
        user.is_consultant = True
        
        user.save(using =self._db)
        return user


    def create_superuser(self, email , prenom ,nom,password = None):
        user = self.create_user(email,prenom,nom,password)
        user.is_staff = True
        user.is_superuser = True
        
        user.save(using =self._db)
        return user



class UserAccount(AbstractBaseUser,PermissionsMixin): 
    email = models.EmailField(max_length=255,unique=True)
    prenom = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    

    is_active = models.BooleanField(default=True)
    is_staff   =models.BooleanField(default=False)
    is_consultant  =models.BooleanField(default=False)
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['prenom','nom']    

