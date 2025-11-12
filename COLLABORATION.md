# 🤝 Guide de Collaboration et Bonnes Pratiques

Ce document définit les règles de travail pour garantir une collaboration efficace, professionnelle et traçable sur le projet **Plateforme Éducative**.

## 🌳 Stratégie de Branches (Gitflow Simplifié)

Nous utilisons une structure stricte pour organiser le développement et éviter les conflits.

### Branches Principales
- **`main`** 🔴 : Code **stable** et **livrable**. C'est la version de production.
    - *Interdiction de commit direct.*
    - *Mise à jour uniquement via Pull Request depuis `develop`.*
- **`develop`** 🟠 : Branche d'**intégration**. C'est la version de développement en cours.
    - *Interdiction de commit direct.*
    - *C'est ici que toutes les fonctionnalités sont rassemblées pour être testées.*

### Branches de Travail
Chaque membre travaille sur sa propre branche, créée à partir de `develop`.

- **`feature/nom-fonctionnalite`** ✨ : Pour ajouter une nouvelle fonctionnalité.
    - *Exemple : `feature/authentification-etudiant`, `feature/ajout-cours`*
- **`fix/nom-bug`** 🐛 : Pour corriger un bug.
    - *Exemple : `fix/correction-login`, `fix/style-bouton`*
- **`docs/sujet`** 📚 : Pour la documentation uniquement.
    - *Exemple : `docs/mise-a-jour-readme`*

---

## 📝 Format des Commits (Conventional Commits)

Pour que l'historique soit lisible et que le professeur puisse voir qui a fait quoi, nous utilisons la convention **Conventional Commits**.

**Format obligatoire :** `type(portée): description courte`

### Types Autorisés
- **feat** : Nouvelle fonctionnalité 🚀
- **fix** : Correction de bug 🩹
- **docs** : Documentation uniquement 📝
- **style** : Formatage, CSS, espaces (pas de changement de code logique) 🎨
- **refactor** : Amélioration du code sans changer le comportement ♻️
- **test** : Ajout ou correction de tests ✅
- **chore** : Maintenance, config, build (ex: gitignore, ci.yml) 🔧

### Exemples
- `feat(auth): ajout de la page de connexion`
- `fix(navbar): correction du lien vers l'accueil`
- `docs(readme): ajout des instructions d'installation`
- `test(auth): ajout du test de login`

---

## 🔄 Processus de Pull Request (PR)

On ne fusionne **jamais** son propre code sans relecture.

1.  **Créer la PR** : De ta branche `feature/...` vers `develop` (PAS vers main !).
2.  **Titre explicite** : Utiliser le format des commits (ex: `feat: Création page profil`).
3.  **Description** : Expliquer ce qui a été fait, lister les fichiers changés importants.
4.  **Reviewers** : Assigner au moins **un autre membre** du groupe pour relire.
5.  **Validation** :
    - Le code doit passer les tests automatiques (CI).
    - Le reviewer doit approuver ("Approve").
6.  **Merge** : Une fois validé, "Squash and merge" ou "Merge commit".

---

## 📋 Gestion de Projet

- Utilisez l'onglet **Issues** pour créer des tickets avant de commencer à coder.
- Assignez-vous ("Assignees") à l'issue sur laquelle vous travaillez.
- Liez la PR à l'issue (ex: "Closes #12" dans la description de la PR).
