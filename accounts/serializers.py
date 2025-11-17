from rest_framework import serializers
from .models import Compte
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class StudentRegSerializer(serializers.ModelSerializer):
    # serializer pour l'inscription
    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Compte
        fields = ['id', 'email', 'password', 'nom', 'prenom']

    def create(self, validated_data):
        # On fait à la main pour être sur
        password = validated_data.pop('password')
        user = Compte(**validated_data)
        user.set_password(password)
        user.role = "STUDENT" # on force le role ici
        user.save()
        return user


class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Ajout des trucs dans le token
        token['email'] = user.email
        token['role'] = "TEACHER" if user.role == "ADMIN" else user.role
        token['nom'] = user.nom
        token['prenom'] = user.prenom
        
        return token
