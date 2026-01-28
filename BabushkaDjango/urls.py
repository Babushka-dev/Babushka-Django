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
from rest_api.endpointsProfile import *
from rest_api.endpointsCategory import *
from django.urls import path

urlpatterns = [
    path("health", health),
  
    path("recipes", manage_recipe),
    path("recipes/<int:id>/image", get_recipe_image),
    path("recipes/<int:recipe_id>/favorite", toggle_favorite),
  
    path('users/me/recipes', get_created_recipes),
    path('users/me/favorites', get_favorite_recipes),
    path('users/me/info', get_user_info),
  
    path('users', create_user),
    path('sessions', login_user),
    
    path("categories", get_categories),
    path("categories/<int:category_id>/image", get_category_image), 
]
