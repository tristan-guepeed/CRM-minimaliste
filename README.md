# CRM Minimaliste

Un système de gestion de relation client (CRM) développé avec Django, permettant de gérer efficacement vos clients avec des fonctionnalités CRUD complètes et un tableau de bord de visualisation.

## Fonctionnalités

- **Authentification complète** : Inscription, connexion et gestion des utilisateurs avec tokens JWT
- **Gestion des clients** : Créer, lire, mettre à jour et supprimer des informations clients
- **API RESTful** : Accès programmatique à toutes les fonctionnalités du CRM
- **Dashboard** : Visualisation des données clients via une interface web intuitive
- **Conteneurisation Docker** : Déploiement facile avec Docker et PostgreSQL

## Prérequis

- Docker et Docker Compose
- Git

## Installation et démarrage

### Cloner le dépôt

```bash
git clone https://github.com/votre-username/crm-minimaliste.git
cd crm-minimaliste
```

### Lancer l'application avec Docker

1. Construire et démarrer les conteneurs Docker:

```bash
docker-compose up -d
```

Cette commande va:
- Créer une base de données PostgreSQL
- Configurer l'environnement Django
- Appliquer les migrations de base de données
- Démarrer le serveur Django sur http://localhost:8000

2. Pour voir les logs:

```bash
docker-compose logs -f
```

## Utilisation

### Interface Web

Accédez à l'application via votre navigateur à l'adresse: http://localhost:8000

- **Page d'accueil**: `/`
- **Tableau de bord clients**: `/dashboard/`
- **Administration**: `/admin/`

### API RESTful

L'API est accessible à la racine `/api/`:

- **Authentification**:
  - POST `/api/auth/register/`: Créer un nouvel utilisateur
  - POST `/api/auth/login/`: Obtenir un token JWT
  - POST `/api/auth/refresh/`: Rafraîchir un token JWT

- **Clients**:
  - GET `/api/clients/`: Liste de tous les clients
  - GET `/api/clients/<id>/`: Détails d'un client spécifique
  - POST `/api/clients/`: Créer un nouveau client
  - PUT `/api/clients/<id>/`: Mettre à jour un client existant
  - DELETE `/api/clients/<id>/`: Supprimer un client

### Format des requêtes API

Pour créer un client (exemple):

```json
POST /api/clients/
Authorization: Bearer <votre_token_jwt>
Content-Type: application/json

{
  "nom": "Dupont",
  "prenom": "Jean",
  "email": "jean.dupont@exemple.fr",
  "telephone": "0123456789",
  "entreprise": "ACME Inc.",
  "notes": "Client premium"
}
```

## Développement

### Structure du projet

```
crm-minimaliste/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
├── crm/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── clients/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
└── authentication/
    ├── models.py
    ├── views.py
    ├── serializers.py
    └── urls.py
```

### Commandes utiles

- Créer un super utilisateur:
  ```bash
  docker-compose exec web python manage.py createsuperuser
  ```

- Appliquer des migrations:
  ```bash
  docker-compose exec web python manage.py makemigrations
  docker-compose exec web python manage.py migrate
  ```

- Accéder au shell Django:
  ```bash
  docker-compose exec web python manage.py shell
  ```

## Arrêt et nettoyage

- Arrêter les conteneurs:
  ```bash
  docker-compose down
  ```

- Arrêter les conteneurs et supprimer les volumes (efface toutes les données):
  ```bash
  docker-compose down -v
  ```

## Informations supplémentaires

- Base de données: PostgreSQL 16
- Backend: Django 5.0 avec Django REST framework
- Authentification: JWT (JSON Web Tokens)

## Dépannage

Si vous rencontrez des problèmes, vérifiez les logs Docker:

```bash
docker-compose logs -f
```

Pour les problèmes d'accès à la base de données, assurez-vous que:
1. Le service PostgreSQL est bien démarré
2. Les variables d'environnement sont correctement configurées
3. Les migrations ont bien été appliquées