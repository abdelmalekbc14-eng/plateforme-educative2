from django.shortcuts import render, redirect
import requests

def call_api(method, path, token=None, data=None, params=None):
    url = f"http://localhost:8000/api{path}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # Simple et direct
    if method == "GET":
        r = requests.get(url, headers=headers, params=params)
    else:
        r = requests.post(url, headers=headers, json=data)
        
    try:
        return r.json(), r.status_code, r.ok
    except:
        return {}, r.status_code, False

def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        data, status, ok = call_api("POST", "/auth/login/", data={"email": email, "password": password})
        
        if ok:
            request.session["access_token"] = data.get("access")
            request.session["refresh_token"] = data.get("refresh")
            return redirect("page_liste_cours")
        
        return render(request, "accounts/login.html", {"error": "Indentifiants incorrects"})

    return render(request, "accounts/login.html")

def register_page(request):
    if request.method == "POST":
        data, status, ok = call_api("POST", "/auth/register/", data={
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
            "nom": request.POST.get("nom"),
            "prenom": request.POST.get("prenom")
        })
        
        if ok: return redirect("login")
        return render(request, "accounts/register.html", {"error": "Erreur d'inscription"})
            
    return render(request, "accounts/register.html")

def logout_action(request):
    request.session.flush()
    return redirect("login")

def liste_cours_page(request):
    token = request.session.get("access_token")
    if not token: return redirect("login")
    
    cours, status, ok = call_api("GET", "/cours/", token=token, params={'search': request.GET.get('q')})
    
    if not ok:
         if status == 401: return redirect("logout")
         cours = []
    
    # Filtrage simple en Python
    q = request.GET.get('q', '').lower()
    if q and isinstance(cours, list):
        cours = [c for c in cours if q in c.get('titre', '').lower()]

    return render(request, "cours/liste_cours.html", {"cours_list": cours})

def create_cours_page(request):
    token = request.session.get("access_token")
    if not token: return redirect("login")
    
    if request.method == "POST":
        data, status, ok = call_api("POST", "/cours/", token=token, data={
            "titre": request.POST.get("titre"),
            "description": request.POST.get("description"),
            "categorie": request.POST.get("categorie"),
            "niveau": request.POST.get("niveau"),
            "niveau_diff": request.POST.get("niveau_diff"),
        })
        if ok: return redirect("page_detail_cours", course_id=data['id'])
        return render(request, "cours/create_cours.html", {"error": "Erreur création"})
    
    return render(request, "cours/create_cours.html")

def detail_cours_page(request, course_id):
    token = request.session.get("access_token")
    if not token: return redirect("login")

    cours, _, ok = call_api("GET", f"/cours/{course_id}/", token=token)
    if not ok: return redirect("page_liste_cours")

    commentaires, _, _ = call_api("GET", f"/messaging/commentaires/?cours_id={course_id}", token=token)
    
    if request.method == "POST" and request.POST.get("message"):
        call_api("POST", "/messaging/commentaires/", token=token, data={
            "cours_id": course_id,
            "cours_titre": cours.get("titre"),
            "message": request.POST.get("message")
        })
        return redirect("page_detail_cours", course_id=course_id)

    statut = None
    if ok:
        data, _, k = call_api("GET", f"/cours/{course_id}/mon-statut/", token=token)
        if k: statut = data.get("statut")
    
    return render(request, "cours/detail_cours.html",{
        "cours": cours,
        "commentaires": commentaires or [],
        "inscription_status": statut
    })

def demander_inscription_cours(request, course_id):
    token = request.session.get("access_token")
    if not token: return redirect("login")
    
    call_api("POST", f"/cours/{course_id}/demander-inscription/", token=token, data={})
    return redirect("page_detail_cours", course_id=course_id)

def mes_cours_page(request):
    token = request.session.get("access_token")
    if not token: return redirect("login")
    
    cours, _, _ = call_api("GET", "/cours/mes-cours/", token=token)
    return render(request, "cours/mes_cours.html", {"cours_list": cours or []})

def gerer_inscriptions_page(request):
    token = request.session.get("access_token")
    if not token: return redirect("login")
    
    inscriptions, _, ok = call_api("GET", "/cours/inscriptions/", token=token)
    
    if ok and isinstance(inscriptions, list):
        inscriptions = [i for i in inscriptions if i['statut'] == "EN_ATTENTE"]
    
    return render(request, "cours/gerer_inscriptions.html", {"inscriptions": inscriptions or []})

def traiter_inscription(request, inscription_id, action):
    token = request.session.get("access_token")
    if not token: return redirect("login")
    
    call_api("POST", f"/cours/inscriptions/{inscription_id}/{action}/", token=token)
    return redirect("gerer_inscriptions_page")

def emploi_du_temps_page(request):
    token = request.session.get("access_token")
    if not token: return redirect("login")
    
    seances, _, _ = call_api("GET", "/timetable/seances/emploi-du-temps/", token=token)
    return render(request, "timetable/emploi_du_temps.html", {"seances": seances or []})

def add_seance_page(request):
    token = request.session.get("access_token")
    if not token: return redirect("login")
    
    if request.method == "POST":
        payload = {
            "cours_id": request.POST.get("cours"),
            "cours_titre": request.POST.get("cours_titre_hidden"),
            "type": request.POST.get("type"),
            "date_debut": request.POST.get("date_debut"),
            "date_fin": request.POST.get("date_fin"),
            "salle": request.POST.get("salle")
        }
        
        # Petit hack pour le titre
        if payload["cours_id"] and not payload.get("cours_titre"):
             c, _, _ = call_api("GET", f"/cours/{payload['cours_id']}/", token=token)
             if c: payload["cours_titre"] = c["titre"]

        data, _, ok = call_api("POST", "/timetable/seances/", token=token, data=payload)
        if ok: return redirect("page_emploi_du_temps")
        
        all_cours, _, _ = call_api("GET", "/cours/", token=token)
        return render(request, "timetable/add_seance.html", {"cours_list": all_cours or [], "error": "Erreur ajout"})
    
    all_cours, _, _ = call_api("GET", "/cours/", token=token)
    return render(request, "timetable/add_seance.html", {"cours_list": all_cours or []})
