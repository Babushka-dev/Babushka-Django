from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Recipe, UserFavoriteRecipes, User, Session

from django.db.models import Exists, OuterRef, Value, BooleanField, Count
from django.db.models.functions import Coalesce


@csrf_exempt
def get_created_recipes(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    user_id = get_user_id_from_token(request)
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'Invalid or missing token'}, status=401)

    page = request.GET.get('page', 0)
    size = request.GET.get('size', 6)

    try:
        page = int(page)
        size = int(size)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'page, size and userIdFav must be integers'}, status=400)

    if page < 0 or size <= 0:
        return JsonResponse({'status': 'error', 'message': 'Invalid page or size'}, status=400)

    favorites_subquery = UserFavoriteRecipes.objects.filter(
        user_id=user_id,
        recipe_id=OuterRef('pk')
    )

    recipes_qs = (
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
    data = list(recipes_qs[start:end])

    return JsonResponse(
        {
            'status': 'success',
            'count': len(data),
            'data': data
        },
        status=200
    )

@csrf_exempt
def get_favorite_recipes(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    user_id = get_user_id_from_token(request)
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'Invalid or missing token'}, status=401)

    page = request.GET.get('page', 0)
    size = request.GET.get('size', 6)

    try:
        page = int(page)
        size = int(size)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'page and size must be integers'}, status=400)

    if page < 0 or size <= 0:
        return JsonResponse({'status': 'error', 'message': 'Invalid page or size'}, status=400)

    recipes_qs = (
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
    data = list(recipes_qs[start:end])

    return JsonResponse(
        {
            'status': 'success',
            'count': len(data),
            'data': data
        },
        status=200
    )


@csrf_exempt
def get_user_info(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    user_id = get_user_id_from_token(request)
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'Invalid or missing token'}, status=401)

    user = (
        User.objects
        .filter(id=user_id)
        .annotate(
            recipes_count=Count('recipe', distinct=True),
            favorites_count=Count('userfavoriterecipes', distinct=True)
        )
        .values(
            'id',
            'username',
            'recipes_count',
            'favorites_count'
        )
        .first()
    )

    if not user:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

    return JsonResponse(
        {
            'status': 'success',
            'data': {
                'id': user['id'],
                'username': user['username'],
                'recipesCount': user['recipes_count'],
                'favoriteRecipesCount': user['favorites_count']
            }
        },
        status=200
    )


def get_user_id_from_token(request):
    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        token = auth.replace("Bearer ", "")
    else:
        return None

    try:
        session = Session.objects.get(token=token)
    except Session.DoesNotExist:
        return None

    return session.user_id