from django.db import models

# ================
#   COURS
# ================
# Service indépendant : pas de lien ForeignKey vers Auth User

class Cours(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    niveau = models.CharField(max_length=50)              # ex : L1, L2, M1...
    niveau_diff = models.CharField(max_length=50)         # ex : Débutant, Intermédiaire...
    categorie = models.CharField(max_length=100)          # ex : Réseau, Dev, Cisco...
    date_creation = models.DateTimeField(auto_now_add=True)

    # Info Prof (denormalisé car service auth séparé)
    prof_id = models.IntegerField()
    prof_email = models.EmailField()
    prof_nom = models.CharField(max_length=100)
    prof_prenom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.titre} ({self.prof_prenom} {self.prof_nom})"


# ================
#   INSCRIPTION
# ================

class Inscription(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = "EN_ATTENTE", "En attente"
        ACCEPTEE = "ACCEPTEE", "Acceptée"
        REFUSEE = "REFUSEE", "Refusée"

    # Lien vers Cours (interne au service)
    cours = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name="inscriptions",
    )

    # Info Étudiant (denormalisé)
    etudiant_id = models.IntegerField()
    etudiant_email = models.EmailField()
    etudiant_nom = models.CharField(max_length=100)
    etudiant_prenom = models.CharField(max_length=100)

    date_demande = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(blank=True, null=True)
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.EN_ATTENTE,
    )

    # Champs du formulaire
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    matricule = models.CharField(max_length=50)
    faculte = models.CharField(max_length=100)
    annee_etude = models.CharField(max_length=50)
    motivation = models.TextField(blank=True, null=True)

    class Meta:
        # Un étudiant ne peut s'inscrire qu'une fois au même cours
        unique_together = ("etudiant_id", "cours")

    def __str__(self):
        return f"Inscrip {self.etudiant_email} -> {self.cours.titre} ({self.statut})"
