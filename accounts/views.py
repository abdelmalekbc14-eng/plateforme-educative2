from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Compte
from .serializers import StudentRegSerializer, CustomTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Login avec JWT
class MyTokenObtainPairView(TokenObtainPairView):
    # on utilise notre serializer custom
    serializer_class = CustomTokenSerializer


# recupérer mon profil
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            # print("User requesting profile: ", user.email)
            
            data = {
                "id": user.id,
                "email": user.email,
                "nom": user.nom,
                "prenom": user.prenom,
                "role": "TEACHER" if user.role == "ADMIN" else user.role,
            }
            return Response(data)
        except Exception as e:
            # print(e)
            return Response({"error": "Erreur inconnue"}, status=500)

class RegisterStudentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Petite validation manuelle au cas où
        email = request.data.get('email')
        if '@' not in email:
             return Response({"error": "Email invalide"}, status=400)

        serializer = StudentRegSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            return Response({
                "message": "User created successfully",
                "user": {
                    "email": user.email,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Pages pour le test (frontend basic)

def register_page(request):
    if request.method == "POST":
        # on récupère les données du form
        prenom = request.POST.get("prenom")
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # creation dirty
        if Compte.objects.filter(email=email).exists():
            return render(request, "accounts/register.html", {"error": "Email existe deja"})

        Compte.objects.create_user(
            email=email,
            password=password,
            nom=nom,
            prenom=prenom
        )

        return redirect("login") # redirect vers login

    return render(request, "accounts/register.html")


def login_page(request):
    # fonction de login classique
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # print(f"Login attempt for {email}")

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect("page_liste_cours")

        return render(request, "accounts/login.html", {"error": "Mauvais credentials"})

    return render(request, "accounts/login.html")
