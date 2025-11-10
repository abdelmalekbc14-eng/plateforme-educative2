# 🎓 Guide de Démarrage pour Débutant

Pas de panique ! C'est normal d'être perdu au début. Ce guide va t'expliquer étape par étape ce que nous faisons et comment mettre ton projet en ligne.

## 1. C'est quoi tout ça ? 🤔

Ton prof te demande de travailler "comme des pros". Voici les outils qu'on utilise :

*   **GitHub** : C'est comme un Google Drive pour ton code. Ça sauvegarde ton travail et permet de travailler à plusieurs.
*   **Git** : C'est le logiciel sur ton ordinateur qui envoie les fichiers vers GitHub.
*   **CI/CD (GitHub Actions)** : C'est un **robot** 🤖. À chaque fois que tu envoies ton code sur GitHub, ce robot se réveille, installe ton projet, et vérifie qu'il n'y a pas de bugs.
*   **SonarQube** : C'est un **correcteur automatique**. Il lit ton code et te dit si tu as mal écrit des choses ou si c'est compliqué à comprendre.
*   **Tests (Pytest)** : Ce sont des petits programmes qui vérifient que ton application fonctionne (ex: est-ce que 1+1 fait bien 2 ?).

## 2. Ce que j'ai déjà fait pour toi ✅

J'ai créé des fichiers "de configuration" dans ton dossier. Tu n'as pas besoin d'y toucher pour l'instant, mais voici à quoi ils servent :

*   `README.md` : La page d'accueil de ton projet (ce que les gens lisent en premier).
*   `.github/workflows/ci.yml` : Le cerveau du robot 🤖. Il contient les instructions pour tester ton code.
*   `sonar-project.properties` : Les réglages pour le correcteur SonarQube.
*   `requirements.txt` : La liste des ingrédients (librairies) dont ton projet a besoin pour fonctionner.

## 3. Ce que TU dois faire maintenant (La partie importante !) 🚀

Tu as créé ton compte GitHub, c'est super. Maintenant, il faut relier ton dossier sur ton PC à GitHub.

### Étape A : Créer le dépôt sur Internet
1.  Va sur [github.com](https://github.com) et connecte-toi.
2.  En haut à droite, clique sur le **+** et choisis **New repository** (Nouveau dépôt).
3.  Nom du dépôt : `plateforme-educative2` (ou ce que tu veux).
4.  Laisse "Public" coché.
5.  **NE COCHE RIEN D'AUTRE** (pas de "Add a README", pas de .gitignore).
6.  Clique sur le bouton vert **Create repository**.

### Étape B : Envoyer ton code (Ligne de commande)
Une fois le dépôt créé, GitHub te montre une page avec des commandes bizarres. Ne t'inquiète pas, on va les faire ensemble.

Ouvre un terminal dans ton dossier `plateforme-educative2` (là où tu es) et tape ces commandes une par une (appuie sur Entrée à chaque fois) :

1.  **Initialiser Git** (dire "ce dossier est un projet") :
    ```bash
    git init
    ```

2.  **Ajouter tes fichiers** (préparer la valise 🧳) :
    ```bash
    git add .
    ```

3.  **Valider** (fermer la valise avec une étiquette "Premier envoi") :
    ```bash
    git commit -m "Mon premier commit : configuration du projet"
    ```

4.  **Renommer la branche principale** (standard moderne) :
    ```bash
    git branch -M main
    ```

5.  **Relier à GitHub** (remplace `TON_PSEUDO` par ton vrai pseudo GitHub !) :
    ```bash
    git remote add origin https://github.com/TON_PSEUDO/plateforme-educative2.git
    ```
    *(Cette commande exacte est affichée sur la page GitHub que tu viens de créer, tu peux la copier-coller de là-bas).*

6.  **Envoyer vers Internet** 🚀 :
    ```bash
    git push -u origin main
    ```

Si on te demande ton mot de passe, attention ! GitHub n'utilise plus le mot de passe du compte pour le terminal, mais un "Token". Si ça bloque ici, dis-le moi, on réglera ça.

## 4. Vérifier que ça marche 🎉

Une fois le `git push` terminé :
1.  Actualise la page de ton projet sur GitHub.
2.  Tu devrais voir tous tes fichiers !
3.  Clique sur l'onglet **Actions** en haut. Tu verras ton robot 🤖 (le pipeline) en train de travailler (ça tournera peut-être en vert ou rouge, c'est normal pour un début).

---
**Si tu bloques à une étape, dis-moi exactement quel message d'erreur tu as !**
