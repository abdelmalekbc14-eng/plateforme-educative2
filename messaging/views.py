from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .models import Commentaire
from .serializers import CommentaireSerializer


class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all().order_by("-date_message")
    serializer_class = CommentaireSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        # Filtre par cours_id (format: ?cours_id=123)
        cid = self.request.query_params.get("cours_id")
        if cid:
            qs = qs.filter(cours_id=cid)
        return qs

    def perform_create(self, serializer):
        # On remplit les infos de l'auteur depuis le JWT
        user = self.request.user
        serializer.save(
            auteur_id=user.id,
            auteur_email=user.email,
            auteur_nom=user.nom,
            auteur_prenom=user.prenom
        )
