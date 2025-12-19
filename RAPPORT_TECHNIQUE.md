# 📘 Rapport de Projet : Ingénierie Logicielle & Plateforme Microservices

**Membres du Groupe** : [Votre Nom/Groupe]
**Date** : 19 Décembre 2025
**Contexte** : Projet Académique de Fin de Module

---

## 📑 Sommaire Exécutif

Ce document retrace la réalisation de notre plateforme éducative distribuée. Au-delà de l'aspect purement technique (développement Python/Django), ce rapport met l'accent sur **l'organisation du travail**, la **méthodologie de développement** (DevOps) et les **choix d'architecture** qui ont permis de mener ce projet à bien dans un contexte collaboratif.

---

## 1. 🤝 Organisation et Méthodologie

Pour répondre aux exigences d'un projet d'ingénierie moderne, nous avons abandonné l'approche artisanale pour adopter des processus industriels.

### 1.1. Gestion de Version Avancée (Git Flow)
Travailler en équipe sur un même code source nécessite une rigueur absolue pour éviter les conflits et les pertes de données. Nous avons mis en place la stratégie **Git Flow** :

*   **Branche `main` (Production)** : Contient uniquement le code stable, validé et testé. C'est l'image de ce qui serait déployé chez le client.
*   **Branche `develop` (Intégration)** : C'est notre zone de travail commune. Toutes les fonctionnalités validées y sont fusionnées.
*   **Branches `feature/*` (Développement)** : Chaque nouvelle tâche (ex: "Création du service Emploi du temps") est développée dans une branche isolée (ex: `feature/timetable`).
    *   *Avantage* : Cela permet à chaque membre de travailler sans bloquer les autres.

### 1.2. Processus de Validation (Code Review)
Aucun code n'est intégré directement sur `main`. Nous avons simulé un processus de **Pull Requests (PR)**.
Avant de fusionner une branche :
1.  Le développeur pousse son code.
2.  Les tests automatiques (CI) se lancent.
3.  Si les tests passent, la fusion est autorisée.
Ce processus garantit que **la branche principale reste toujours verte** (fonctionnelle).

---

## 2. ⚙️ Industrialisation et Qualité (CI/CD)

Le rôle de l'ingénieur n'est pas seulement d'écrire du code, mais de garantir sa maintenabilité. Nous avons délégué la vérification de la qualité à un automate : **GitHub Actions**.

### 2.1. Le Pipeline d'Intégration Continue
À chaque modification du code, notre pipeline CI (défini dans `.github/workflows/ci.yml`) exécute une série de contrôles stricts :

1.  **Installation de l'environnement** : Le projet est redéployé à neuf sur un serveur distant (Ubuntu) pour vérifier qu'il ne manque aucune dépendance (`requirements.txt`).
2.  **Linting (Flake8)** : Analyse statique du code pour vérifier le respect des normes PEP8. Cela assure que tout le code du projet semble avoir été écrit par une seule personne, facilitant la relecture.
3.  **Tests Automatisés (Pytest)** : Exécution des tests unitaires et d'intégration.
    *   *Sécurité* : Nous vérifions qu'un étudiant ne peut pas créer de cours (Erreur 403).
    *   *Logique* : Nous vérifions que l'emploi du temps récupère bien les données des cours.

### 2.2. Métriques de Qualité (SonarCloud)
Nous avons connecté notre dépôt à **SonarCloud** pour obtenir des métriques objectives sur notre travail :
*   **Recherche de Bugs** : Détection automatique d'erreurs potentielles.
*   **Dette Technique** : Estimation du temps nécessaire pour corriger les mauvaises pratiques.
*   **Couverture de Code** : Mesure du pourcentage de code vérifié par les tests.
*   *Quality Gate* : Nous avons défini des seuils bloquants (le pipeline échoue si la qualité n'est pas au rendez-vous).

---

## 3. 🏗 Architecture Logicielle Distribuée

Le choix des **Microservices** n'est pas qu'un choix technique, c'est aussi un choix **organisationnel**.

### 3.1. Découpage par Domaines Métier
L'application est divisée en services autonomes, ce qui permet de paralléliser le développement :

*   **Service Accounts** : Authentification centralisée (JWT).
*   **Service Cours** : Gestion du catalogue académique.
*   **Service Timetable** : Gestion des plannings.
*   **Service Messaging** : Communication asynchrone.
*   **Frontend** : Interface utilisateur unique.

### 3.2. Pourquoi ce choix ?
Dans une équipe, ce découpage permet à un développeur A de travailler sur l'algorithme de l'emploi du temps (Timetable) pendant qu'un développeur B améliore le design du Frontend, sans qu'ils ne se marchent sur les pieds (fichiers différents, dépôts virtuels séparés).

### 3.3. Communication et Résilience
Nous avons mis en œuvre deux modes de communication :
1.  **Synchrone (HTTP)** : Pour les données immédiates.
2.  **Asynchrone (RabbitMQ)** : Pour décorréler les services.
    *   *Exemple de gestion* : Lorsqu'un cours est créé, un message est envoyé. Si le service de notification est en panne, le message est stocké dans la file d'attente (Queue) et sera traité au redémarrage. C'est une architecture **tolérante aux pannes**.

---

## 4. 🚀 Déploiement et Environnement

### 4.1. Conteneurisation (Docker)
L'usage de Docker a permis de standardiser nos environnements de développement. Plus de "ça marche chez moi mais pas chez toi". Chaque service tourne dans son conteneur isolé.

### 4.2. Configuration Centralisée
Nous avons appliqué le principe des "12-Factor App" en externalisant toute la configuration (adresses IP, clés secrètes, ports) dans des variables d'environnement (`.env`).
Cela nous a permis lors de la démonstration finale de déployer l'architecture sur **plusieurs machines physiques (Multi-PC)** en changeant simplement une ligne de configuration, sans toucher au code source.

---

## 5. Conclusion et Retour d'Expérience

Ce projet a été l'occasion de confronter la théorie à la pratique.

**Ce que nous avons appris** :
*   La complexité de gérer des transactions distribuées (Microservices).
*   L'importance vitale de la CI/CD pour éviter les régressions en fin de projet.
*   La rigueur nécessaire dans la gestion des branches Git.

Nous livrons aujourd'hui une plateforme fonctionnelle, mais surtout une **base de code saine, testée et documentée**, prête pour une évolution future ou une reprise par une autre équipe.
