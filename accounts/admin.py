from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Compte


@admin.register(Compte)
class CompteAdmin(UserAdmin):
    model = Compte

    list_display = ("email", "nom", "prenom", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informations personnelles", {"fields": ("nom", "prenom")}),
        ("Rôle et permissions", {
            "fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Dates importantes", {"fields": ("last_login", "date_creation")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nom", "prenom", "role", "password1", "password2"),
        }),
    )

    search_fields = ("email", "nom", "prenom")
    ordering = ("email",)
