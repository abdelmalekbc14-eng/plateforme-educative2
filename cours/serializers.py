# cours/serializers.py

from rest_framework import serializers
from .models import Cours, Inscription

class CoursSerializer(serializers.ModelSerializer):
    prof_nom_complet = serializers.SerializerMethodField()

    class Meta:
        model = Cours
        fields = [
            "id",
            "titre",
            "description",
            "niveau",
            "niveau_diff",
            "categorie",
            "date_creation",
            "prof_id",
            "prof_email",
            "prof_nom",
            "prof_prenom",
            "prof_nom_complet",
        ]
        # Ces champs sont remplis automatiquement par le JWT dans la vue
        read_only_fields = [
            "id", 
            "date_creation", 
            "prof_id", 
            "prof_email", 
            "prof_nom", 
            "prof_prenom", 
            "prof_nom_complet"
        ]

    def get_prof_nom_complet(self, obj):
        return f"{obj.prof_prenom} {obj.prof_nom}"


class InscriptionSerializer(serializers.ModelSerializer):
    cours_titre = serializers.CharField(source="cours.titre", read_only=True)

    class Meta:
        model = Inscription
        fields = [
            "id",
            "cours",
            "cours_titre",
            "etudiant_id",
            "etudiant_email",
            "etudiant_nom",
            "etudiant_prenom",
            "date_demande",
            "date_validation",
            "statut",
            "nom",
            "prenom",
            "matricule",
            "faculte",
            "annee_etude",
            "motivation",
        ]
        read_only_fields = [
            "id",
            "etudiant_id",
            "etudiant_email",
            "etudiant_nom",
            "etudiant_prenom",
            "date_demande",
            "date_validation",
            "statut",
            "cours_titre",
        ]