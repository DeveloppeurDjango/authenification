from django.db import models

# Create your models here.
class ContactForm(models.Model):
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f'{self.nom} {self.prenoms} - {self.sujet}'
