# Babushka

**Babushka** is a recipe-sharing application created by four students as a study project. The idea is simple: users can create recipes, browse recipes from other users, save favorites, and organize recipes by categories.

The project is split into three parts:

- **Babushka Android**: the mobile app used by users.
- **Babushka Django**: the active backend API used by the Android app.
- **Babushka Spring**: the first backend version, kept as a legacy project after the backend was moved to Django.

# Babushka Django

Babushka Django is the active backend server for the project. It provides the REST API used by the Android client for authentication, recipe browsing, recipe creation, favorites, categories, profile data, and image loading.

## Project Pair

- [**Babushka Android**](https://github.com/Babushka-dev/Babushka-Android): the mobile client that users interact with.
- [**Babushka Django**](https://github.com/Babushka-dev/Babushka-Django): this active backend REST API.
- [**Babushka Spring**](https://github.com/Babushka-dev/Babushka-Spring): the old backend prototype, kept for reference.

The Android app is configured to call this backend locally at:

```text
http://10.0.2.2:8000/
```

The Django server itself runs locally at:

```text
http://localhost:8000/
```

## Features

- Health check endpoint.
- User registration.
- User login with session token creation.
- Token-based protected endpoints using the `Authorization: Bearer <token>` header.
- Recipe creation by authenticated users.
- Recipe list loading.
- Recipe search by title.
- Recipe filtering by category.
- Pagination with `page` and `size` query parameters.
- Recipe image serving.
- Category list loading.
- Category image serving.
- Favorite and unfavorite actions.
- Current user's created recipes.
- Current user's favorite recipes.
- Current user's profile information and recipe counters.

## Tech Stack

- Python.
- Django 5.2.
- Django function-based views.
- PostgreSQL.
- JSON REST endpoints.
- Binary image responses for recipe and category images.
- Token sessions stored in the database.

## Main Structure

```text
Babushka-backend-django/
  BabushkaDjango/
    settings.py       Django settings and database configuration
    urls.py           API route registration
    asgi.py
    wsgi.py

  rest_api/
    endpointsUser.py      Registration and login endpoints
    endpointsRecipe.py    Recipe list, creation, images, favorites, health
    endpointsProfile.py   Current user profile, own recipes, favorite recipes
    endpointsCategory.py  Categories and category images
    helpers.py            Token lookup and pagination helpers
    models.py             Existing database table mappings
```

## Local Requirements

- Python with Django installed.
- PostgreSQL database with the Babushka tables.
- Database access configured in `BabushkaDjango/settings.py`.

The current settings use PostgreSQL:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "babushka_db",
        "USER": "babushka",
        "PASSWORD": "PUT_YOUR_PASSWORD_HERE",
        "HOST": "82.26.150.189",
        "PORT": "5432",
    }
}
```

For local development, update these values to match your own PostgreSQL user, password, host, and database.

## Running Locally

From the backend module:

```bash
cd Babushka-Django
python manage.py runserver
```

On Windows:

```powershell
cd Babushka-Django
python manage.py runserver
```

After startup, the API is available at:

```text
http://localhost:8000/
```

## API Overview

System:

- `GET /health`

Authentication:

- `POST /users`
- `POST /sessions`

Recipes:

- `GET /recipes`
- `POST /recipes`
- `GET /recipes/<id>/image`
- `POST /recipes/<recipe_id>/favorite`

Profile:

- `GET /users/me/info`
- `GET /users/me/recipes`
- `GET /users/me/favorites`

Categories:

- `GET /categories`
- `GET /categories/<category_id>/image`

## Request Notes

Protected endpoints expect the session token in this format:

```text
Authorization: Bearer <sessionToken>
```

Recipe list endpoints support pagination:

```text
GET /recipes?page=0&size=6
```

Recipes can also be searched and filtered:

```text
GET /recipes?search=pasta
GET /recipes?categoryId=2
GET /recipes?page=0&size=6&search=pasta&categoryId=2
```

The favorite endpoint uses a query parameter:

```text
POST /recipes/5/favorite?favorite=true
POST /recipes/5/favorite?favorite=false
```
