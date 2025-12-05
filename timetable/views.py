import requests
from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Seance
from .serializers import SeanceSerializer
from .permissions import IsTeacher

class SeanceViewSet(viewsets.ModelViewSet):
    queryset = Seance.objects.all().order_by("date_debut")
    serializer_class = SeanceSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        cid = self.request.query_params.get("cours_id")
        if cid:
            return Seance.objects.filter(cours_id=cid).order_by("date_debut")
        return Seance.objects.all().order_by("date_debut")

    @action(detail=False, methods=["get"], url_path="emploi-du-temps")
    def emploi_du_temps(self, request):
        user = request.user
        base_url = settings.COURS_SERVICE_BASE_URL
        headers = {"Authorization": request.META.get("HTTP_AUTHORIZATION")}

        ids = []

        if user.role == "TEACHER":
            r = requests.get(f"{base_url}/mes-cours/", headers=headers)
            if r.ok:
                ids = [c["id"] for c in r.json()]

        elif user.role == "STUDENT":
            r = requests.get(f"{base_url}/mes-inscriptions-ids/", headers=headers)
            if r.ok:
                ids = r.json().get("cours_ids", [])
        
        seances = Seance.objects.filter(cours_id__in=ids).order_by("date_debut")
        return Response(self.get_serializer(seances, many=True).data)