# timetable/models.py

from django.db import models


class Seance(models.Model):
    class TypeSeance(models.TextChoices):
        COURS = "COURS", "Cours"
        TD = "TD", "Travaux dirigés"
        TP = "TP", "Travaux pratiques"

    # Référence au service Cours via ID (plus de ForeignKey)
    cours_id = models.IntegerField()
    cours_titre = models.CharField(max_length=200)

    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    type = models.CharField(max_length=10, choices=TypeSeance.choices)
    salle = models.CharField(max_length=50)
    remarque = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.cours_titre} - {self.type} - {self.date_debut}"
