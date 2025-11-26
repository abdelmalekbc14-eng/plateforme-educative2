from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cours, Inscription
from .serializers import CoursSerializer, InscriptionSerializer
from .permissions import IsTeacher
import pika
import json

# Fonction pour publier l'événement dans RabbitMQ
def publish_inscription_event(data):
    # Connexion à RabbitMQ
    from platforme_educatif.settings import RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASS
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        channel = connection.channel()

        # Déclarer la queue 'inscriptions' si elle n'existe pas
        channel.queue_declare(queue='inscriptions', durable=True)

        # Publier un message dans la queue
        channel.basic_publish(
            exchange='',
            routing_key='inscriptions',
            body=json.dumps(data),  # Données sous forme JSON
            properties=pika.BasicProperties(
                delivery_mode=2,  # Message persistant
            )
        )

        connection.close()
    except Exception as e:
        print(f"Erreur RabbitMQ: {e}")

class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all().order_by("-date_creation")
    serializer_class = CoursSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # On verifie si c'est un prof pour créer/modifier
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # J'ajoute IsTeacher pour qu'on soit sur
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        # On attache le prof connecté au cours
        user = self.request.user
        serializer.save(
            prof_id=user.id,
            prof_email=user.email,
            prof_nom=user.nom,
            prof_prenom=user.prenom
        )

    @action(detail=True, methods=["post"], url_path="demander-inscription")
    def demander_inscription(self, request, pk=None):
        cours = self.get_object()
        user = request.user

        # Vérification du rôle de l'utilisateur
        if getattr(user, "role", None) != "STUDENT":
            return Response({"detail": "Pas autorisé"}, status=403)

        # Récupérer les données de la demande d'inscription
        data = request.data

        # Créer l'inscription ou vérifier si elle existe déjà
        inscription, created = Inscription.objects.get_or_create(
            etudiant_id=user.id,
            cours=cours,
            defaults={
                "etudiant_email": user.email,
                "etudiant_nom": user.nom,
                "etudiant_prenom": user.prenom,
                "nom": data.get("nom", user.nom),
                "prenom": data.get("prenom", user.prenom),
                "matricule": data.get("matricule", ""),
                "faculte": data.get("faculte", ""),
                "annee_etude": data.get("annee_etude", ""),
                "motivation": data.get("motivation", ""),
            },
        )

        # Si l'inscription existe déjà, retourner un message d'erreur
        if not created:
            return Response({"detail": "Déjà inscrit"}, status=400)

        # Publier un message dans RabbitMQ
        publish_inscription_event({
            "etudiant_email": user.email,
            "cours_id": cours.id,
            "cours_titre": cours.titre
        })

        # Réponse après inscription réussie
        return Response(
            {"detail": "Demande envoyée", "statut": inscription.statut, "cours": cours.titre},
            status=status.HTTP_201_CREATED
        )


    @action(detail=True, methods=["get"], url_path="mon-statut")
    def mon_statut(self, request, pk=None):
        cours = self.get_object()
        try:
            ins = Inscription.objects.get(etudiant_id=request.user.id, cours=cours)
            return Response({"statut": ins.statut})
        except Inscription.DoesNotExist:
            return Response({"statut": None})

    @action(detail=False, methods=["get"], url_path="mes-cours")
    def mes_cours(self, request):
        user = request.user
        role = getattr(user, "role", None)
        
        if role == "TEACHER" or role == "ADMIN":
            cours = Cours.objects.filter(prof_id=user.id)
            return Response(self.get_serializer(cours, many=True).data)

        elif role == "STUDENT":
            inscriptions = Inscription.objects.filter(
                etudiant_id=user.id,
                statut=Inscription.Statut.ACCEPTEE,
            ).select_related("cours")
            cours = [i.cours for i in inscriptions]
            return Response(self.get_serializer(cours, many=True).data)
            
        return Response({"detail": "Rôle inconnu"}, status=403)

    @action(detail=False, methods=["get"], url_path="mes-inscriptions-ids")
    def mes_inscriptions_ids(self, request):
        user = request.user
        if getattr(user, "role", None) != "STUDENT":
             return Response({"cours_ids": []})
        
        ids = Inscription.objects.filter(
            etudiant_id=user.id,
            statut=Inscription.Statut.ACCEPTEE
        ).values_list('cours_id', flat=True)
        
        return Response({"cours_ids": list(ids)})


class InscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Inscription.objects.filter(
            cours__prof_id=self.request.user.id
        ).order_by("-date_demande")

    @action(detail=True, methods=["post"], url_path="accepter")
    def accepter(self, request, pk=None):
        ins = self.get_object()
        if ins.cours.prof_id != request.user.id:
            return Response({"detail": "Interdit"}, status=403)

        ins.statut = Inscription.Statut.ACCEPTEE
        ins.date_validation = timezone.now()
        ins.save()
        return Response({"detail": "Acceptée", "statut": ins.statut})

    @action(detail=True, methods=["post"], url_path="refuser")
    def refuser(self, request, pk=None):
        ins = self.get_object()
        if ins.cours.prof_id != request.user.id:
            return Response({"detail": "Interdit"}, status=403)

        ins.statut = Inscription.Statut.REFUSEE
        ins.date_validation = timezone.now()
        ins.save()
        return Response({"detail": "Refusée", "statut": ins.statut})
