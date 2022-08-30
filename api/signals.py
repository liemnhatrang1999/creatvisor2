from urllib import request
from django.db.models.signals import post_save, pre_delete,m2m_changed
from api.serializer import User
from api.models import Atelier, Certification, Exp, Formation, Info_consultant,Avis, Info_entrepreneur, UserAccount
from django.dispatch import receiver


@receiver(post_save,sender=Formation)
def save_formation(sender,instance,created,*args, **kwargs):
    if created :
        import inspect
        request = None
        for fr in inspect.stack():
            if fr[3] == 'get_response':
                request = fr[0].f_locals['request']
                break
        current_logged_in_user = request.user
        objet = Info_consultant.objects.filter(user = current_logged_in_user.id)
        # objet.update(formation=instance.id)
        print(objet)
        objet2 = objet.first()
        print(objet2)
        objet2.formation.add(instance.id)

@receiver(post_save,sender=Exp)
def save_exp(sender,instance,created,*args, **kwargs):
    if created :
        import inspect
        request = None
        for fr in inspect.stack():
            if fr[3] == 'get_response':
                request = fr[0].f_locals['request']
                break
        current_logged_in_user = request.user
        objet = Info_consultant.objects.filter(user = current_logged_in_user.id)
        # objet.update(formation=instance.id)
        objet2 = objet.first()
        objet2.exp.add(instance.id)


@receiver(post_save,sender=Certification)
def save_certification(sender,instance,created,*args, **kwargs):
    if created :
        import inspect
        request = None
        for fr in inspect.stack():
            if fr[3] == 'get_response':
                request = fr[0].f_locals['request']
                break
        current_logged_in_user = request.user
        objet = Info_consultant.objects.filter(user = current_logged_in_user.id)
        # objet.update(formation=instance.id)
        objet2 = objet.first()
        objet2.certification.add(instance.id)

from django.db.models.signals import post_save, pre_delete
from api.models import  Info_consultant, Info_entrepreneur, UserAccount



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
        
from django.db.models.signals import m2m_changed
from api.models import Info_consultant,Avis




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

