import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users
import json

# Utilizamos la libería re (regular expression) para poder crear expresiones regulares
# En este caso, la usaremos para validar el nombre de usuario.
 # Solo se podrán utilizar letras mayúsculas y minúsculas A-Z, números 1-9, guion y guion bajo.
USERNAME_REGEX = re.compile(r'^[A-Za-z0-9_-]+$')

# FUNCIÓN CREAR USUARIO
@csrf_exempt
def create_user(request):
    if request.method != 'POST': # Si el método no es un POST: ERROR
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
        return JsonResponse({'status': 'error', 'message': 'Username may only include letters, numbers, dash and underscore'}, status=400)

    # Si la contraseña no está en el intervalo [6,20] (inclusives)
    if len(password) > 20 or len(password) < 6:
        return JsonResponse({'status': 'error', 'message': 'Password must be at least 6 characters and not more than 20'}, status=400)

    # Si el usuario ya existe
    if Users.objects.filter(username=username).exists():
        return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)

    # Creamos el usuario
    user = Users.objects.create(username=username, password=password, active=True)

    return JsonResponse({'message': 'User registered successfully', 'user_id': user.id}, status=201)
