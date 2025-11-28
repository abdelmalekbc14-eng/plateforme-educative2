from django.contrib import admin
from .models import Commentaire

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ("cours_titre", "cours_id", "auteur_email", "date_message")
    search_fields = ("cours_titre", "auteur_email", "message")
