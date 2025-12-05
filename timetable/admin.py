# timetable/admin.py

from django.contrib import admin
from .models import Seance


@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    """
    Admin pour les séances.
    On utilise cours_titre et cours_id car il n'y a plus de ForeignKey vers cours.Cours.
    """
    list_display = ("cours_titre", "cours_id", "type", "date_debut", "date_fin", "salle")
    list_filter = ("type",)  # tu peux ajouter "cours_id" si tu veux filtrer par id
    search_fields = ("cours_titre", "salle")
