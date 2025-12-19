from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Commentaire

User = get_user_model()

class MessagingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com", 
            password="password", 
            nom="Test", 
            prenom="User",
            role="STUDENT"
        )
        self.client.force_authenticate(user=self.user)
        
        self.commentaire = Commentaire.objects.create(
            cours_id=1,
            cours_titre="Maths",
            auteur_id=self.user.id,
            auteur_email=self.user.email,
            auteur_nom=self.user.nom,
            auteur_prenom=self.user.prenom,
            message="Super cours"
        )

    def test_list_commentaires(self):
        response = self.client.get('/api/messaging/commentaires/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_commentaires_by_cours(self):
        response = self.client.get('/api/messaging/commentaires/?cours_id=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        response_empty = self.client.get('/api/messaging/commentaires/?cours_id=999')
        self.assertEqual(len(response_empty.data), 0)

    def test_create_commentaire(self):
        data = {
            "cours_id": 2,
            "cours_titre": "Physique",
            "message": "Nouveau message"
        }
        response = self.client.post('/api/messaging/commentaires/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Commentaire.objects.count(), 2)
        # Verify automatic author assignment
        self.assertEqual(response.data['auteur_email'], self.user.email)
