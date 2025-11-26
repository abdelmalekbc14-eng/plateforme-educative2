# cours/permissions.py

from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    """
    Autorise seulement les profs (role = TEACHER).
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (getattr(user, "role", None) == "TEACHER" or getattr(user, "role", None) == "ADMIN")
        )
