from django.test import TestCase
from .models import Cours

class CoursTests(TestCase):
    def test_simple_cours_creation(self):
        """Simplest test to ensure CI passes"""
        cours = Cours.objects.create(
            titre="Test Course",
            description="Desc",
            niveau="L1",
            niveau_diff="Facile",
            categorie="Dev",
            prof_id=1,
            prof_email="prof@test.com",
            prof_nom="Prof",
            prof_prenom="Test"
        )
        self.assertEqual(cours.titre, "Test Course")
