from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Manager pour les comptes
# J'ai copié ça d'un tuto sur internet
class CompteManager(BaseUserManager):

    def create_user(self, email, password=None, **other_fields):
        # Verification l'email
        if not email:
            raise ValueError('Il faut une adresse email !!')

        email = self.normalize_email(email)
        
        # par defaut c'est un etudiant
        role_par_defaut = "STUDENT"

        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **other_fields):
        # création de l'admin
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('role', 'ADMIN')

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be staff')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be superuser')

        return self.create_user(email, password, **other_fields)


class Compte(AbstractBaseUser, PermissionsMixin):

    # J'utilise TextChoices c'est mieux
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Étudiant"
        TEACHER = "TEACHER", "Professeur"
        ADMIN = "ADMIN", "Administrateur"

    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    
    # le role de l'utilisateur
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    date_creation = models.DateTimeField(auto_now_add=True)

    objects = CompteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return self.email
