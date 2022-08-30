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
