from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Recipe, UserFavoriteRecipes, User

from django.db.models import Exists, OuterRef, Value, BooleanField, Count
from django.db.models.functions import Coalesce


@csrf_exempt
def get_created_recipes(request, user_id):
    if request.method != 'GET':
        return JsonResponse(
            {'status': 'error', 'message': 'Method not allowed'},
            status=405
        )

    page = request.GET.get('page', 0)
    size = request.GET.get('size', 6)
    user_id_fav = request.GET.get('userIdFav')

    try:
        page = int(page)
        size = int(size)
    except Exception:
        return JsonResponse(
            {'status': 'error', 'message': 'page and size must be integers'},
            status=400
        )

    if page < 0 or size <= 0:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid page or size'},
            status=400
        )

    favorites_subquery = UserFavoriteRecipes.objects.filter(
        user_id=user_id_fav,
        recipe_id=OuterRef('pk')
    )

    recipes = (
        Recipe.objects
        .filter(active=True, user_id=user_id)
        .annotate(
            is_favorite=Coalesce(
                Exists(favorites_subquery),
                Value(False),
                output_field=BooleanField()
            )
        )
        .values(
            'id',
            'title',
            'description',
            'ingredients',
            'preparation',
            'difficulty',
            'is_favorite'
        )
    )

    start = page * size
    end = start + size
    data = list(recipes[start:end])

    return JsonResponse(
        {'status': 'success', 'count': len(data), 'data': data},
        status=200
    )


@csrf_exempt
def get_favorite_recipes(request, user_id):
    if request.method != 'GET':
        return JsonResponse(
            {'status': 'error', 'message': 'Method not allowed'},
            status=405
        )

    page = request.GET.get('page', 0)
    size = request.GET.get('size', 6)

    try:
        page = int(page)
        size = int(size)
    except Exception:
        return JsonResponse(
            {'status': 'error', 'message': 'page and size must be integers'},
            status=400
        )

    if page < 0 or size <= 0:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid page or size'},
            status=400
        )

    recipes = (
        Recipe.objects
        .filter(
            active=True,
            userfavoriterecipes__user_id=user_id
        )
        .annotate(
            is_favorite=Value(True, output_field=BooleanField())
        )
        .values(
            'id',
            'title',
            'description',
            'ingredients',
            'preparation',
            'difficulty',
            'is_favorite'
        )
    )

    start = page * size
    end = start + size
    data = list(recipes[start:end])

    return JsonResponse(
        {'status': 'success', 'count': len(data), 'data': data},
        status=200
    )

