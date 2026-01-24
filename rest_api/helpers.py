from .models import Session

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