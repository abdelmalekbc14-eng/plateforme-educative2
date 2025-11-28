from rest_framework import serializers
from .models import Commentaire

class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = [
            "id",
            "cours_id",
            "cours_titre",
            "auteur_id",
            "auteur_email",
            "auteur_nom",
            "auteur_prenom",
            "message",
            "date_message",
        ]
        read_only_fields = [
            "id",
            "auteur_id",
            "auteur_email",
            "auteur_nom",
            "auteur_prenom",
            "date_message",
        ]
