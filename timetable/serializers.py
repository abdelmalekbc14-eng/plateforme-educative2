from rest_framework import serializers
from .models import Seance


class SeanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seance
        fields = [
            "id",
            "cours_id",
            "cours_titre",
            "date_debut",
            "date_fin",
            "type",
            "salle",
            "remarque",
        ]
        read_only_fields = ["id"]
