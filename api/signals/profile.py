from django.db.models.signals import post_save, pre_delete
from api.serializer import User
from api.models import  Info_consultant, Info_entrepreneur, UserAccount
from django.dispatch import receiver



@receiver(pre_delete, sender=UserAccount)
def delete_profile(sender, instance,*args, **kwargs):
    if instance.is_consultant ==True:
        objet =Info_consultant.objects.filter(user=instance.id)
        objet.delete()
    else:
        objet =Info_entrepreneur.objects.filter(user=instance.id)
        objet.delete()

@receiver(post_save,sender=UserAccount)
def save_profile(sender,instance,created,*args, **kwargs):
    if created :
        if instance.is_consultant ==True :
            objet = Info_consultant.objects.create()
            objet.save()
            objet.user.add(instance.id)
        if instance.is_superuser!=False:
            objet = Info_entrepreneur.objects.create()
            objet.save()
            objet.user.add(instance.id)
        

