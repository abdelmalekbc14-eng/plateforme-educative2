from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Seance
from unittest.mock import patch

User = get_user_model()

class TimetableTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            email="prof@test.com", 
            password="password", 
            nom="Prof", 
            prenom="Test",
            role="TEACHER"
        )
        self.student = User.objects.create_user(
            email="student@test.com", 
            password="password", 
            nom="Student", 
            prenom="Test",
            role="STUDENT"
        )
        
        self.seance = Seance.objects.create(
            cours_id=1,
            cours_titre="Maths",
            date_debut=timezone.now(),
            date_fin=timezone.now() + timezone.timedelta(hours=2),
            type="COURS",
            salle="A101"
        )

    def test_create_seance_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        data = {
            "cours_id": 1,
            "cours_titre": "Maths",
            "date_debut": timezone.now(),
            "date_fin": timezone.now() + timezone.timedelta(hours=2),
            "type": "TD",
            "salle": "B202"
        }
        response = self.client.post('/api/timetable/seances/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_seance_student_unauthorized(self):
        self.client.force_authenticate(user=self.student)
        data = {
            "cours_id": 1,
            "cours_titre": "Maths",
            "date_debut": timezone.now(),
            "date_fin": timezone.now() + timezone.timedelta(hours=2),
            "type": "TD",
            "salle": "B202"
        }
        response = self.client.post('/api/timetable/seances/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('timetable.views.requests.get')
    def test_emploi_du_temps_teacher(self, mock_get):
        # Mock response from Cours Service
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = [{"id": 1, "titre": "Maths"}]
        
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get('/api/timetable/seances/emploi-du-temps/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should see seance for cours_id=1
        self.assertEqual(len(response.data), 1)

    @patch('timetable.views.requests.get')
    def test_emploi_du_temps_student(self, mock_get):
        # Mock response from Cours Service (mes-inscriptions-ids)
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {"cours_ids": [1]}
        
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/timetable/seances/emploi-du-temps/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
