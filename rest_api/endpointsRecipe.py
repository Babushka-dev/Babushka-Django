import json
import base64

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .helpers import get_user_id_from_token, use_page_system
from .models import Recipe

# Función según petición recibida
@csrf_exempt
def manage_recipe(request):
    if request.method == 'POST':
        return create_recipe(request)
    elif request.method == 'GET':
        return get_recipes(request)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def create_recipe(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    user_id = get_user_id_from_token(request)
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'Invalid or missing token'}, status=401)

    # Extraemos información del JSON
    title = data.get('title')
    description = data.get('description')
    ingredients = data.get('ingredients')
    preparation = data.get('preparation')
    difficulty = data.get('difficulty')
    image_base64 = data.get('imageBase64')
    time = data.get('time')

    # Si title, difficulty o time están vacíos
    if not title:
        return JsonResponse({'status': 'error', 'message': 'Title is required'}, status=400)
    if not difficulty:
        return JsonResponse({'status': 'error', 'message': 'Difficulty is required'}, status=400)
    if not time:
        return JsonResponse({'status': 'error', 'message': 'Time is required'}, status=400)

    # Si time no es integer
    if not str(time).isdigit():
        return JsonResponse({'status': 'error', 'message': 'Time must be an integer'}, status=400)
    time = int(time)

    # Si difficulty no es integer
    if not str(difficulty).isdigit():
        return JsonResponse({'status': 'error', 'message': 'Difficulty must be an integer'}, status=400)
    difficulty = int(difficulty)

    # Si difficulty no está en el rango entre 1 y 5
    if difficulty < 1 or difficulty > 5:
        return JsonResponse({'status': 'error', 'message': 'Difficulty must be between 1 and 5'}, status=400)

    # Si title tiene más de 25 caracteres
    if len(title) > 50:
        return JsonResponse({'status': 'error', 'message': 'Title cannot exceed 50 characters'}, status=400)

    # Creamos la receta (sin guardar)
    recipe = Recipe(
        title=title,
        description=description,
        ingredients=ingredients,
        preparation=preparation,
        time=time,
        difficulty=difficulty,
        user_id=user_id,
        active=True
    )

    # Procesamos la imagen Base64
    if image_base64:
        try:
            recipe.image = base64.b64decode(image_base64)
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'Invalid imageBase64'}, status=400)

    # Guardamos en la base de datos
    recipe.save()

    # Respuesta correcta
    return JsonResponse(
        {
            'message': 'Recipe created successfully',
            'recipe_id': recipe.id
        },
        status=201
    )

def get_recipes(request):
    # Obtenemos solo las recetas activas
    recipes = Recipe.objects.filter(active=True)

    # Búsqueda
    search = request.GET.get('search')
    if search:
        recipes = recipes.filter(title__icontains=search)

    # Filtro por categoría
    category_id = request.GET.get('categoryId')
    if category_id:
        if not str(category_id).isdigit():
            return JsonResponse( {'status': 'error', 'message': 'category must be an integer'}, status=400)
        recipes = recipes.filter(recipecategories__category_id = category_id)

    pg = use_page_system(request, recipes)
    if 0 in pg:
        return pg.get(0)  # Recibir cuerpo del error
    else:
        recipes = pg.get(1)  # Recibe todas recetas con paginación

    # Sacar userId del usuario
    user_id = get_user_id_from_token(request)
    favorites = []
    if user_id:
        # Recibir recetas favoritas de userId
        favorites = Recipe.objects.filter(userfavoriterecipes__user_id=user_id)

    # Convertimos las recetas a lista de diccionarios
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
            'isFavorite': recipe in favorites, # Comprobar si receta está en el array (en boleeano)
        })
    return JsonResponse({'status': 'success', 'count': len(data), 'data': data}, status=200)


@csrf_exempt
def get_recipe_image(request, id):
    # Solo GET
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    # Buscamos la receta activa por id
    recipe = Recipe.objects.filter(id=id, active=True).first()

    if not recipe:
        return JsonResponse({'status': 'error', 'message': 'Recipe not found'}, status=404)

    # Si no tiene imagen
    if not recipe.image:
        return JsonResponse({'status': 'error', 'message': 'Recipe has no image'}, status=404)

    # Devolvemos los bytes de la imagen (bytea)
    return HttpResponse(recipe.image, content_type='image/jpeg')


@csrf_exempt
def health(request):
    return JsonResponse({'status': 'ok'})
