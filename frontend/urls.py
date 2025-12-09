from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_action, name="logout"),

    # Cours
    path("", views.liste_cours_page, name="page_liste_cours"), # Accueil = liste cours
    path("cours/<int:course_id>/", views.detail_cours_page, name="page_detail_cours"),
    path("cours/create/", views.create_cours_page, name="create_cours_page"),
    path("cours/mes-cours/", views.mes_cours_page, name="page_mes_cours"),
    path("cours/<int:course_id>/inscription/", views.demander_inscription_cours, name="demander_inscription_cours"),
    
    # Inscriptions (Prof)
    path("inscriptions/", views.gerer_inscriptions_page, name="gerer_inscriptions_page"),
    path("inscriptions/<int:inscription_id>/<str:action>/", views.traiter_inscription, name="traiter_inscription"),

    # Timetable
    path("emploi-du-temps/", views.emploi_du_temps_page, name="page_emploi_du_temps"),
    path("emploi-du-temps/ajouter/", views.add_seance_page, name="add_seance_page"),
]
