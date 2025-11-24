from django.contrib import admin
from .models import Cours, Inscription


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    # On affiche des infos simples disponibles dans le modèle
    list_display = (
        "titre",
        "categorie",
        "niveau",
        "prof_nom",
        "prof_prenom",
        "prof_email",
        "date_creation",
    )
    search_fields = ("titre", "categorie", "prof_nom", "prof_prenom", "prof_email")
    list_filter = ("categorie", "niveau", "niveau_diff")


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "etudiant_email",
        "etudiant_nom",
        "cours",
        "statut",
        "date_demande",
        "date_validation",
    )
    search_fields = ("etudiant_email", "etudiant_nom", "cours__titre")
    list_filter = ("statut", "date_demande")
