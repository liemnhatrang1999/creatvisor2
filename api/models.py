from cgitb import text
import email
from pydoc import describe
from pyexpat import model
import site

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from twilio.rest import Client


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
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using =self._db)
        return user

class UserAccount(AbstractBaseUser,PermissionsMixin): 
    email = models.EmailField(max_length=255,unique=True)
    prenom = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    is_consultant  = models.BooleanField(default=False)
    is_averti  = models.IntegerField(default=0)
    is_interdit =  models.BooleanField(default=False)
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['prenom','nom','phone']    

class Thematique_metier(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self) :
        return self.nom

class Info_entrepreneur(models.Model):
    photo = models.ImageField( upload_to='media', height_field=None, width_field=None, max_length=None,blank=True)
    valeur_humaine = models.TextField()
    secteur = models.CharField(max_length=255)
    problematique = models.TextField()
    project = models.TextField(blank=True)
    user = models.ManyToManyField(UserAccount, related_name="info_entrepreneur")

    def __str__(self) :
        L=[]
        user= self.user.all()
        if len(user)!=0:
            for p in user:
                L.append(p)
            B = f"{L[0]}"
            B = B.split(":")        
            return B[0]
        return(" oui")

class Competance (models.Model):
    nom = models.CharField(max_length=50)
    def __str__(self):
        return self.nom


class Formation(models.Model):
    nom_diplome = models.CharField(max_length=50)
    annee = models.IntegerField(default=0)
    description = models.TextField()
    ecole = models.CharField(max_length=50)
    is_encours = models.BooleanField(default=True)
    # consultant = models.ManyToManyField(Infà_, related_name="info_consultant")

    def __str__(self) :
        return self.nom_diplome

class Certification(models.Model):
    nom_certification = models.CharField(max_length=50)
    organisme = models.CharField(max_length=50)
    annee = models.IntegerField()
    lien_certification = models.URLField()
    is_encours = models.BooleanField(default=False)
    location = models.CharField(max_length=50)
    def __str__(self) :
            return self.nom_certification

class Exp(models.Model):
    societe = models.CharField(max_length=50)
    secteur_activite = models.CharField(max_length=50)
    titre = models.CharField(max_length=50)
    is_freelance = models.BooleanField(default=False)
    location = models.CharField(max_length=50)
    is_encours = models.BooleanField(default=False)
    date_debut = models.DateField()
    date_fin = models.DateField()
    def __str__(self) :
            return self.titre

class Info_consultant(models.Model):
    photo = models.ImageField( upload_to='media', height_field=None, width_field=None, max_length=None,blank = True)
    experiences = models.IntegerField(default=0)
    competances = models.ManyToManyField(Competance,related_name="info_consultant",blank=True)
    valeur_humaine = models.TextField(blank=True)
    user = models.ManyToManyField(UserAccount, related_name="info_consultant",blank=True)
    localisation = models.TextField(blank=True)
    tarif = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    site_web =models.URLField(max_length=200,blank=True)
    note_moyenne = models.DecimalField(max_digits=5, decimal_places=2,blank=True,default=0)
    nb_avis = models.IntegerField(blank=True,default=0)
    formation = models.ManyToManyField(Formation, related_name="info_consultant",)
    certification = models.ManyToManyField(Certification, related_name="info_consultant",blank=True)
    exp = models.ManyToManyField(Exp, related_name="info_consultant",blank=True)

    def __str__(self) :
        L=[]
        user= self.user.all()
        if len(user)!=0:

            for p in user:
                L.append(p)
            B = f"{L[0]}"
            B = B.split(":")
            
            return B[0]
        return("consultant")

# class Formation(models.Model):
#     nom_diplome = models.CharField(max_length=50)
#     annee = models.IntegerField(default=0)
#     description = models.TextField()
#     ecole = models.CharField(max_length=50)
#     is_encours = models.BooleanField(default=True)
#     consultant = models.ForeignKey(Info_consultant, on_delete=models.CASCADE)

#     def __str__(self) :
#         return self.nom_diplome

class Atelier(models.Model):
    nom = models.CharField(max_length=255)
    pre_requis = models.TextField(max_length=10000,default="")
    thematique_metier = models.ManyToManyField(Thematique_metier,related_name='atelier')
    participants = models.ManyToManyField(Info_entrepreneur,related_name="atelier",blank=True,)
    creator = models.ManyToManyField(Info_consultant,related_name="atelier",)
    created_date = models.DateTimeField (auto_now_add = True)
    expires_date =models.DateTimeField()
    is_gratuit = models.BooleanField(default=False)
    def __str__(self) :
        return self.nom

class Avis(models.Model):
    user = models.ManyToManyField(UserAccount,related_name='avis')
    ponctualite = models.DecimalField(max_digits=5, decimal_places=2)
    respect = models.DecimalField(max_digits=5, decimal_places=2)
    qualite = models.DecimalField(max_digits=5, decimal_places=2)
    atelier = models.ManyToManyField(Atelier, related_name="avis")
    commentaire = models.TextField()
    moyenne_atelier = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    info_consultant = models.ManyToManyField(Info_consultant,related_name='avis',blank=True)
    def __str__(self) :
        return self.commentaire

class Partenaire(models.Model):
    nom = models.CharField(max_length=255)
    description= models.TextField()
    logo = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None,blank = True)
    thematique_metier = models.ManyToManyField(Thematique_metier,related_name="partenaire")

    def __str__(self):
        return self.nom
    
