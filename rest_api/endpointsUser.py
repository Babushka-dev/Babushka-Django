import re
import secrets
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Session

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


@csrf_exempt
def login_user(request):
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
