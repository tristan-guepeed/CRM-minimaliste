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
cd crm
```

### Lancer l'application avec Docker

1. Construire et démarrer les conteneurs Docker:

```bash
docker-compose build
```

```bash
docker-compose up -d
```

Ces commandes vont:
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
  - POST `/register/`: Créer un nouvel utilisateur
  - POST `/login/`: Obtenir un token JWT
  - POST `/api/token/refresh/`: Rafraîchir un token JWT

- **Clients**:
  - GET `/clients/`: Liste de tous les clients
  - GET `/clients/<uuid>/`: Détails d'un client spécifique
  - POST `/clients/create`: Créer un nouveau client
  - PUT `/clients/<uuid>/`: Mettre à jour un client existant
  - DELETE `/clients/<uuid>/`: Supprimer un client

### Format des requêtes API

Pour créer un client (exemple):

```json
POST clients/create/
Authorization: Bearer <votre_token_jwt>
Content-Type: application/json

{
  "first_name": "Jean",
  "last_name": "Dupont",
  "email": "jean.dupont@exemple.fr",
  "phone_number": "0123456789",
  "adress": "124 Rue Malmort"
}
```

## Développement

### Structure du projet

```
CRM-minimaliste
    ├── README.md
    └── crm
        ├── Dockerfile
        ├── clients
        │   ├── migrations
        │   │   ├── 0001_initial.py
        │   │   └── __init__.py
        │   ├── models.py
        │   ├── serializers.py
        │   ├── templates
        │   │   └── dashboard.html
        │   ├── tests
        │   │   ├── test_create_view.py
        │   │   ├── test_delete_by_id_view.py
        │   │   ├── test_get_all_view.py
        │   │   ├── test_get_by_id_view.py
        │   │   └── test_update_view.py
        │   ├── urls.py
        │   └── views.py
        ├── crm
        │   ├── __init__.py
        │   ├── admin.py
        │   ├── asgi.py
        │   ├── migrations
        │   ├── models.py
        │   ├── serializers.py
        │   ├── settings.py
        │   ├── tests
        │   │   ├── test_login_view.py
        │   │   └── test_register_view.py
        │   ├── urls.py
        │   ├── views.py
        │   └── wsgi.py
        ├── docker-compose.yml
        ├── manage.py
        └── requirements.txt
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
- Backend: Django 5.1 avec Django REST framework
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