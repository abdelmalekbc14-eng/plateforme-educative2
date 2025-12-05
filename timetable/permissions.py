from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    """
    Permission personnalisée : seulement les Profs (TEACHER).
    """

    def has_permission(self, request, view):
        # L'utilisateur doit être authentifié + avoir le rôle TEACHER
        # Le role est dans request.user grace au JWT et l'auth backend
        if not request.user.is_authenticated:
            return False
            
        role = getattr(request.user, "role", None)
        return role == "TEACHER"
