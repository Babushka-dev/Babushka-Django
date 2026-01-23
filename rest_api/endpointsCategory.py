import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category

#  CREAR CATEGORÍA
@csrf_exempt
def create_category(request):
    if request.method != 'POST':  # Si el método no es POST: ERROR
        return JsonResponse(
            {'status': 'error', 'message': 'Method not allowed'},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid JSON'},
            status=400
        )

    name = data.get('name')

    # Si el nombre está vacío
    if not name:
        return JsonResponse(
            {'status': 'error', 'message': 'Missing category name'},
            status=400
        )

    # Si el nombre tiene más de 25 caracteres
    if len(name) > 25:
        return JsonResponse(
            {'status': 'error', 'message': 'Category name cannot be over 25 characters'},
            status=400
        )

    # Si la categoría ya existe
    if Category.objects.filter(name=name).exists():
        return JsonResponse(
            {'status': 'error', 'message': 'Category already exists'},
            status=400
        )

    # Creamos la categoría (active = True por defecto)
    category = Category.objects.create(
        name=name,
        active=True,
        image=data.get('image')
    )

    return JsonResponse(
        {
            'message': 'Category created successfully',
            'category_id': category.id
        },
        status=201
    )
