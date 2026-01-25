from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .helpers import get_user_id_from_token, use_page_system
from .models import Recipe, User

@csrf_exempt
def get_created_recipes(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    user_id = get_user_id_from_token(request)
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'Invalid or missing token'}, status=401)

    recipes = Recipe.objects.filter(active=True, user_id=user_id)

    pg = use_page_system(request, recipes)
    if 0 in pg:
        return pg.get(0)
    else:
        recipes = pg.get(1)

    favorites = Recipe.objects.filter(userfavoriterecipes__user_id=user_id)

    data = []
    for recipe in recipes:
        data.append({
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'preparation': recipe.preparation,
            'time': recipe.time,
            'difficulty': recipe.difficulty,
            'isFavorite': recipe in favorites # Si receta está en el array favorites = receta es favorita (Tipo boolean)
        })
    return JsonResponse({'status': 'success', 'count': len(data), 'data': data}, status=200)

@csrf_exempt
def get_favorite_recipes(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    user_id = get_user_id_from_token(request)
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'Invalid or missing token'}, status=401)

    recipes = Recipe.objects.filter(active=True, userfavoriterecipes__user_id=user_id)

    pg = use_page_system(request, recipes)
    if 0 in pg:
        return pg.get(0)
    else:
        recipes = pg.get(1)

    data = []
    for recipe in recipes:
        data.append({
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'preparation': recipe.preparation,
            'time': recipe.time,
            'difficulty': recipe.difficulty,
            'isFavorite': True # Todas recetas son favoritas
        })
    return JsonResponse({'status': 'success', 'count': len(data), 'data': data}, status=200)

@csrf_exempt
def get_user_info(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    user_id = get_user_id_from_token(request)
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'Invalid or missing token'}, status=401)

    recipes = Recipe.objects.filter(active=True, user_id=user_id)
    favRecipes = Recipe.objects.filter(active=True, userfavoriterecipes__user_id=user_id)
    user = User.objects.get(id=user_id)

    return JsonResponse(
        {
            'status': 'success',
            'data': {
                'id': user.id,
                'username': user.username,
                'countCreatedRecipe': recipes.count(),
                'countFavoriteRecipe': favRecipes.count(),
            }
        },
        status=200
    )