from django.db.models.signals import m2m_changed
from api.serializer import User
from api.models import Info_consultant,Avis
from django.dispatch import receiver




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
