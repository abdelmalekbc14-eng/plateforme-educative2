from rest_framework_simplejwt.tokens import AccessToken

def frontend_user(request):
    """
    Injecte un objet 'user' simulé en décodant le token JWT de la session.
    Permet d'avoir user.role, user.nom, etc. dans les templates.
    """
    if request.path.startswith('/admin/'):
        return {}
        
    token_str = request.session.get("access_token")
    if token_str:
        try:
            token = AccessToken(token_str)
            
            class MockUser:
                is_authenticated = True
                is_staff = False
                is_superuser = False
                # Récupération des claims du token
                id = token.get("user_id")
                role = token.get("role", "STUDENT") # Valeur par défaut
                nom = token.get("nom", "")
                prenom = token.get("prenom", "")
                email = token.get("email", "")
            
            return {"user": MockUser()}
        except Exception:
            # Si le token est invalide on ne fait rien (user restera AnonymousUser)
            pass
            
    return {}
