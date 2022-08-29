import email
from django.db.models.signals import pre_save,post_save, post_delete, pre_delete,m2m_changed

from api.serializer import User
from .models import Atelier, Info_consultant,Avis, Info_entrepreneur, UserAccount
from django.dispatch import receiver

@receiver(pre_delete, sender=UserAccount)
def delete_profile(sender, instance,*args, **kwargs):
    if instance.is_consultant ==True:
        objet =Info_consultant.objects.filter(user=instance.id)
        objet.delete()
    else:
        objet =Info_entrepreneur.objects.filter(user=instance.id)
        objet.delete()

@receiver(m2m_changed, sender=Avis.info_consultant.through)
def save_avis(sender, instance,action,*args, **kwargs):
    if action=="post_add":
        
        objet = Info_consultant.objects.filter(id=list(kwargs["pk_set"])[0])
        # print(objet)
        if objet[0].note_moyenne ==0:
            note_consultant = objet[0].note_moyenne + instance.moyenne_atelier
            counter_avis = objet[0].nb_avis + 1
            objet.update(nb_avis=counter_avis,note_moyenne=note_consultant)
        else :
            note_consultant = (objet[0].note_moyenne + instance.moyenne_atelier)/2
            counter_avis = objet[0].nb_avis + 1
            objet.update(nb_avis=counter_avis,note_moyenne=note_consultant)

@receiver(post_save,sender=UserAccount)
def save_profile(sender,instance,created,*args, **kwargs):
    if created :
        if instance.is_consultant ==True:
            objet = Info_consultant.objects.create()
            objet.save()
            objet.user.add(instance.id)

        else:
            objet = Info_entrepreneur.objects.create()
            objet.save()
            objet.user.add(instance.id)



