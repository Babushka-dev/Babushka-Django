"""
URL configuration for BabushkaDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_api.endpointsFavorites import toggle_favorite
from rest_api.endpointsRecipe import *
from rest_api.endpointsUser import *
from rest_api.endpointsCategory import * #Importa todas las funciones que hay en endpointsCategory.py
from django.urls import path

urlpatterns = [
    path("health", health),
    path("recipes", manage_recipe),
    path("recipes/<int:id>/image", get_recipe_image),
    path("categories", get_categories), #Devuelve el JSON con las categorías
    path("categories/<int:category_id>/image", get_category_image), #Devuelve las imágenes de las categorías
    path('users', create_user),
    path('sessions', login_user),
    path("recipes/<int:recipe_id>/favorite", toggle_favorite),
]