import re
import secrets
import json
import base64

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Session, Recipe

# Utilizamos la libería re (regular expression) para poder crear expresiones regulares
# En este caso, la usaremos para validar el nombre de usuario.
# Solo se podrán utilizar letras mayúsculas y minúsculas A-Z, números 1-9, guion y guion bajo.
USERNAME_REGEX = re.compile(r'^[A-Za-z0-9_-]+$')


# FUNCIÓN CREAR USUARIO
@csrf_exempt
def create_user(request):
    if request.method != 'POST':  # Si el metodo no es un POST: ERROR
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    username = data.get('username')
    password = data.get('password')

    # Si la contraseña o el username están vacíos:
    if not username or not password:
        return JsonResponse({'status': 'error', 'message': 'Missing username or password'}, status=400)

    # Si el username tiene más de 20 caracteres
    if len(username) > 20:
        return JsonResponse({'status': 'error', 'message': 'Username cannot be over 20 characters'}, status=400)

    # Si el username no matchea la expresión regular:
    if not USERNAME_REGEX.match(username):
        return JsonResponse(
            {'status': 'error', 'message': 'Username may only include letters, numbers, dash and underscore'},
            status=400)

    # Si la contraseña no está en el intervalo [6,20] (inclusives)
    if len(password) > 20 or len(password) < 6:
        return JsonResponse(
            {'status': 'error', 'message': 'Password must be at least 6 characters and not more than 20'}, status=400)

    # Si el usuario ya existe
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)

    # Creamos el usuario
    user = User.objects.create(username=username, password=password, active=True)

    return JsonResponse({'message': 'User registered successfully', 'user_id': user.id}, status=201)


# Función según petición recibida
@csrf_exempt
def manage_recipe(request):
    # Comprobamos que el HTTP sea POST
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
        return JsonResponse({'status': 'error', 'message': 'Difficulty must be an integer'}, status=400)
    difficulty = int(difficulty)

    # Si difficulty no está en el rango entre 1 y 5
    if difficulty < 1 or difficulty > 5:
        return JsonResponse({'status': 'error', 'message': 'Difficulty must be between 1 and 5'}, status=400)

    # Si title tiene más de 25 caracteres
    if len(title) > 25:
        return JsonResponse({'status': 'error', 'message': 'Title cannot exceed 50 characters'}, status=400)

    # Creamos la receta (sin guardar)
    recipe = Recipe(
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

@csrf_exempt
def login_user(request):
    if request.method != 'POST':  # Si el método no es un POST: ERROR
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    username = data.get('username')
    password = data.get('password')

    # Si la contraseña o el username están vacíos:
    if not username or not password:
        return JsonResponse({'status': 'error', 'message': 'Missing username or password'}, status=400)

    # Buscamos entre los users si existe alguno con el nombre de usuario
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:  # Si no existe, error
        return JsonResponse({'status': 'error', 'message': 'Username does not exist'}, status=401)

    # Si existe el username, proseguimos y comprobamos si las contraseñas coinciden; si no coinciden, error
    if user.password != password:
        return JsonResponse({'status': 'error', 'message': 'Passwords do not match'}, status=401)

    # Si el usuario no está activo, devolvemos un código de error.
    if not user.active:
        return JsonResponse({'status': 'error', 'message': 'User is not active'}, status=403)
    # generamos un token de 16 bytes que será convertido a hexadecimal
    token = secrets.token_hex(16)

    # Creamos la sesión y le asignamos el token
    session = Session.objects.create(user_id=user.id, token=token)

    # Devolvemos el token de sesión
    return JsonResponse({'sessionToken': token}, status=201)

def get_recipes(request):
    # Obtenemos solo las recetas activas
    recipes = Recipe.objects.filter(active=True)

    # Búsqueda
    search = request.GET.get('search')
    if search:
        recipes = recipes.filter(title__icontains=search)

    # Leemos parámetros opcionales
    page = request.GET.get('page')
    size = request.GET.get('size')

    # Si vienen page y size, aplicamos paginación
    if page is not None and size is not None:
        try:
            page = int(page)
            size = int(size)
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'page and size must be integers'}, status=400)

        if size <= 0:
            return JsonResponse({'status': 'error', 'message': 'size must be greater than 0'}, status=400)
        if page < 0:
            return JsonResponse({'status': 'error', 'message': 'page must be greater than 0'}, status=400)

        # Clave de la paginación
        start = page * size
        end = start + size
        recipes = recipes[start:end]

    # Convertimos las recetas a lista de diccionarios
    data = []
    for recipe in recipes:
        data.append({
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'preparation': recipe.preparation,
            'difficulty': recipe.difficulty,
            'userId': recipe.user.id if recipe.user else None
        })
    return JsonResponse({'status': 'success', 'count': len(data), 'data': data}, status=200)


# FUNCIÓN DESCARGA IMAGEN
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


# FUNCIÓN PRUEBA
@csrf_exempt
def health(request):
    return JsonResponse({'status': 'ok'})
