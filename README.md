# Plateforme Éducative Agile

Ce projet est une application web de plateforme éducative développée dans le cadre du module "Méthodes de Management Agiles". Il met en pratique la méthode SCRUM et les outils DevOps.

## 🛠 Stack Technique

- **Backend** : Django (Python)
- **Frontend** : HTML, CSS, JavaScript (intégrés dans Django)
- **Base de données** : SQLite (Dev) / PostgreSQL (Prod)
- **Tests Unitaires** : PyTest / Django Test
- **Qualité du Code** : SonarQube
- **CI/CD** : GitHub Actions

## 🚀 Fonctionnalités Principales

1.  **Authentification** : Inscription et connexion (Étudiants, Enseignant, Admin).
2.  **Gestion des Cours** : Ajout, modification, suppression et consultation de cours.
3.  **Tableau de Bord** : Vue d'ensemble pour chaque rôle utilisateur.
4.  **Emploi du Temps** : Gestion et affichage des séances de cours.
5.  **Notifications** : Système de messagerie.

## 📦 Installation et Lancement

1.  **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

2.  **Appliquer les migrations** :
    ```bash
    python manage.py migrate
    ```

3.  **Lancer le serveur** :
    ```bash
    python manage.py runserver
    ```

## 🧪 Tests

Lancer les tests unitaires :
```bash
pytest
```

## 🤝 Collaboration

Ce projet suit des règles strictes de collaboration pour garantir la qualité et la traçabilité.

👉 **[Lire le Guide de Collaboration (COLLABORATION.md)](COLLABORATION.md)**

*   **Branches** : Gitflow (`main`, `develop`, `feature/*`)
*   **Commits** : Conventional Commits (ex: `feat: ajout login`)
*   **Pull Requests** : Obligatoires avec review avant fusion
