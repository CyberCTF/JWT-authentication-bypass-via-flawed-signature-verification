# 📦 RULES DU PROJET (Version PRO)

## Objectif
Fournir une structure propre, minimaliste et reproductible pour les applications contenues dans ce dépôt.  
Tout le code applicatif est centralisé sous `build/app/`. Le dossier `build/deploy/` contient les fichiers de déploiement/développement.

## Arborescence obligatoire
- `docker-compose.yml` à la racine (production/base)
- `build/app/` :
  - `Dockerfile`
  - `app.py`
  - `requirements.txt`
  - `parsing/`
  - `templates/*.html`
  - `tests/main.py`
- `build/deploy/` :
  - `README.md` (déploiement/dev)
  - `docker-compose.dev.yml`
- `.github/workflows/docker-publish.yml` : build → test → publish
- `README.md` (racine) : doc principale

## Conventions et règles
- Un seul `requirements.txt` (dans `build/app/`).
- Dockerfile unique : `build/app/Dockerfile`.
- Tests exécutables : `python build/app/tests/main.py`.
- Respecter PEP8.
- Ne pas conserver markdowns inutiles (CONTRIBUTING/TODO/CHANGELOG) sauf s'ils sont activement maintenus.
- Conserver les dossiers de challenges s'ils existent.
- `.gitignore` présent et configuré (exclure artefacts, caches, virtualenvs, build, logs).

## CI/CD
- Le workflow `.github/workflows/docker-publish.yml` :
  - Installe dépendances depuis `build/app/requirements.txt`.
  - Exécute `python build/app/tests/main.py`.
  - Build et publie l'image uniquement si tous les tests passent avec succès.

## Nettoyage / maintenance
- Supprimer les fichiers redondants.
- Corriger les chemins dans Dockerfile/docker-compose après déplacement.
- Mettre à jour la documentation dans `README.md` (racine) et `build/deploy/README.md`.

## Structure du projet JWT Challenge

### Application Core (`build/app/`)
- **Point d'entrée**: `app.py` - Application Flask principale
- **Templates**: `templates/` - Interface utilisateur HTML
- **Tests**: `tests/main.py` - Suite de tests automatisés
- **Dépendances**: `requirements.txt` - Packages Python requis
- **Container**: `Dockerfile` - Configuration de containerisation

### Déploiement (`build/deploy/`)
- **Développement**: `docker-compose.dev.yml` - Environnement de dev avec hot-reload
- **Documentation**: `README.md` - Guide de déploiement détaillé

### Challenge Files
- **Scripts d'exploitation**: Conservés dans le répertoire racine/challenges
- **Documentation technique**: Guides et rapports de sécurité
- **Outils personnalisés**: Extensions Burp Suite, scripts d'analyse

## Standards de qualité

### Code Python
- Respect PEP8 pour la lisibilité
- Documentation des fonctions critiques
- Gestion d'erreurs appropriée
- Tests unitaires couvrant les fonctionnalités principales

### Sécurité
- Vulnérabilités intentionnelles documentées
- Isolation des environnements de test
- Pratiques de développement sécurisé pour le code non-vulnérable
- Documentation des vecteurs d'attaque

### Documentation
- README principal : Vue d'ensemble et quick start
- README déploiement : Guide technique détaillé
- Code commenté pour les parties complexes
- Exemples d'utilisation fournis

## Maintenance continue

### Tests automatisés
- Validation du fonctionnement de l'application
- Vérification de la présence des vulnérabilités
- Tests d'intégration du déploiement
- Contrôle de qualité du code

### CI/CD Pipeline
- Build automatique des images Docker
- Exécution des tests sur chaque commit
- Publication conditionnelle (tests passants uniquement)
- Notifications en cas d'échec

### Gestion des versions
- Versioning sémantique des releases
- Tags Git pour les versions stables
- Changelog automatique
- Images Docker versionnées