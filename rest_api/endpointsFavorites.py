import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .helpers import get_user_id_from_token
from .models import Recipe, User, Session, UserFavoriteRecipes


# Desactiva la protección CSRF porque este endpoint será consumido por una app móvil
@csrf_exempt
def toggle_favorite(request, recipe_id):

    # Comprueba que el metodo HTTP sea POST
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # Obtiene el ID del usuario a partir del token de autenticación
    user_id = get_user_id_from_token(request)

    # Si el token no es válido o no existe, devuelve error 401 (no autorizado)
    if user_id is None:
        return JsonResponse({"error": "Invalid token"}, status=401)

    # Leer JSON del body (?favorite=true o ?favorite=false)
    favorite = request.GET.get('favorite')

    # Si no se ha enviado el parámetro, devuelve error 400 (petición incorrecta)
    if favorite is None:
        return JsonResponse({"error": "Missing isFavorite"}, status=400)

    # Buscar receta
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return JsonResponse({"error": "Recipe not found"}, status=404)

    # Crear o borrar favorito
    if favorite:
        UserFavoriteRecipes.objects.get_or_create(user_id=user_id, recipe_id=recipe_id)
    else:
        UserFavoriteRecipes.objects.filter(user_id=user_id, recipe_id=recipe_id).delete()

    # Devuelve una respuesta JSON confirmando que funciona
    return JsonResponse({
        "message": "Favorite updated",
        "recipeId": recipe_id,
        "isFavorite": favorite
    })
