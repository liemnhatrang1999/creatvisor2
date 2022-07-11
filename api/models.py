from django.db import models

class Client(models.Model):
    nomClient = models.CharField(max_length=240)
    prenomClient = models.CharField(max_length=240)
    emailClient = models.EmailField()
    mobileClient = models.CharField(max_length=20)
    inscriptionClient = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nomClient