from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models.signals import pre_delete




class ListRetraite(models.Model):
    ordre = models.IntegerField(default=0) 
    titre = models.CharField(max_length=8, validators=[RegexValidator(r'^[a-zA-Z0-9]{8}$', 'Le titre doit contenir 8 caractères alphanumériques.')])
    beneficiaire = models.CharField(max_length=255, default='')
    nni = models.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]{10}$', 'Le NNI doit contenir exactement 10 chiffres.')], default='')
    date_retraite = models.DateField()
    ville = models.CharField(max_length=100)
    age = models.IntegerField()
    telephone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
    
    class Meta:
        ordering = ['created_at']


# Signal pour mettre à jour le champ ordre lors de l'enregistrement
@receiver(pre_save, sender=ListRetraite)
def set_ordre(sender, instance, **kwargs):
    if instance.pk is None:
        # Nouvel enregistrement
        max_ordre = ListRetraite.objects.all().aggregate(models.Max('ordre'))['ordre__max']
        if max_ordre is None:
            max_ordre = 0
        instance.ordre = max_ordre + 1
    else:
        # Mise à jour d'un enregistrement existant
        existing_instance = ListRetraite.objects.get(pk=instance.pk)
        if existing_instance.ordre != instance.ordre:
            instance.ordre = existing_instance.ordre

# Signal pour mettre à jour les ordres lors de la suppression
@receiver(pre_delete, sender=ListRetraite)
def update_order_on_delete_retraire(sender, instance, **kwargs):
    # Récupérer tous les objets dont l'ordre est supérieur à celui supprimé
    retraites_to_update = ListRetraite.objects.filter(ordre__gt=instance.ordre)
    for retraite in retraites_to_update:
        # Décrémenter l'ordre de chaque objet
        retraite.ordre -= 1
        retraite.save()  



        
class OperateRetraite(models.Model):
    ordre = models.IntegerField()
    Numero_titre = models.ForeignKey(ListRetraite, on_delete=models.CASCADE, blank=True, null=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    beneficiaire = models.CharField(max_length=255, default='')
    nni = models.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]{10}$', 'Le NNI doit contenir exactement 10 chiffres.')], default='')
    date_operation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.Numero_titre.titre} - Montant: {self.montant}"
    
    class Meta:
        ordering = ['date_operation']
    
@receiver(pre_save, sender=OperateRetraite)
def update_order_on_create(sender, instance, **kwargs):
    if not instance.pk:  # Nouvelle instance
        try:
            last_instance = sender.objects.latest('ordre')
            instance.ordre = last_instance.ordre + 1
        except ObjectDoesNotExist:
            instance.ordre = 1
        



@receiver(pre_delete, sender=(OperateRetraite))
def update_order_on_delete(sender, instance, **kwargs):
    # Obtenez toutes les instances avec un ordre supérieur à celui supprimé
    instances_to_update = sender.objects.filter(ordre__gt=instance.ordre)
    # Décrémentez l'ordre de chaque instance suivante
    for instance_to_update in instances_to_update:
        instance_to_update.ordre -= 1
        instance_to_update.save()
        


