from django.db import models

class Commentaire(models.Model):
    # Données dénormalisées Course (plus de ForeignKey)
    cours_id = models.IntegerField()
    cours_titre = models.CharField(max_length=200)

    # Données dénormalisées Auteur (plus de ForeignKey vers AUTH_USER_MODEL)
    auteur_id = models.IntegerField()
    auteur_email = models.EmailField()
    auteur_nom = models.CharField(max_length=100)
    auteur_prenom = models.CharField(max_length=100)

    message = models.TextField()
    date_message = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auteur_email} - {self.cours_titre}"
