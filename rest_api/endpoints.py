import base64
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_api.models import Recipes

# FUNCIÓN CREAR RECETA
@csrf_exempt
def create_recipe(request):

    # Comprobamos que el HTTP sea POST
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405 )

    # Leer el JSON
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    # Extraemos información del JSON
    title = data.get('title')
    description = data.get('description')
    ingredients = data.get('ingredients')
    preparation = data.get('preparation')
    difficulty = data.get('difficulty')
    image_base64 = data.get('imageBase64')

    # Si title y difficulty están vacíos
    if not title or difficulty is None:
        return JsonResponse({'status': 'error', 'message': 'Title and difficulty are required'}, status=400)

    # Si difficulty no es integer
    if not str(difficulty).isdigit():
        return JsonResponse( {'status': 'error', 'message': 'Difficulty must be an integer'}, status=400)
    difficulty = int(difficulty)

    # Si difficulty no está en el rango entre 1 y 5
    if difficulty < 1 or difficulty > 5:
        return JsonResponse({'status': 'error', 'message': 'Difficulty must be between 1 and 5'}, status=400)

    # Si title tiene más de 50 caracteres
    if len(title) > 50:
        return JsonResponse({'status': 'error', 'message': 'Title cannot exceed 50 characters'},status=400)

    # Creamos la receta (sin guardar)
    recipe = Recipes(
        title=title,
        description=description,
        ingredients=ingredients,
        preparation=preparation,
        difficulty=difficulty,
        active=True
    )

    # Procesamos la imagen Base64
    if image_base64:
        try:
            recipe.image = base64.b64decode(image_base64)
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'Invalid imageBase64'},status=400)

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

@csrf_exempt
def health(request):
    return JsonResponse({'status': 'ok'})