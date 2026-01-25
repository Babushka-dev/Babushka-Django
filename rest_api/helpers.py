from django.http import JsonResponse

from .models import Session

def get_user_id_from_token(request):
    auth = request.headers.get("Authorization") # Sacamos token
    if auth and auth.startswith("Bearer "):
        token = auth.replace("Bearer ", "")
    else:
        return None

    try:
        session = Session.objects.get(token=token)
    except Session.DoesNotExist:
        return None

    return session.user_id

def use_page_system(request, recipes):
    # Leemos parámetros opcionales
    page = request.GET.get('page')
    size = request.GET.get('size')

    # Si vienen page y size, aplicamos paginación
    if page is not None and size is not None:
        try:
            page = int(page)
            size = int(size)
        except Exception:
            return {0 : JsonResponse({'status': 'error', 'message': 'page and size must be integers'}, status=400)}

        if size <= 0:
            return {0 : JsonResponse({'status': 'error', 'message': 'size must be greater than 0'}, status=400)}
        if page < 0:
            return {0 : JsonResponse({'status': 'error', 'message': 'page must be greater than 0'}, status=400)}

        # Clave de la paginación
        start = page * size
        end = start + size
        recipes = recipes[start:end]

    return {1 : recipes}

    # 0 - Error
    # 1 - All OK