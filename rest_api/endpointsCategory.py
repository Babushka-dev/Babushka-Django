import base64 
from django.http import JsonResponse, \
    HttpResponse 
from .models import Category


#Esta función lee todas las categorías de la BD, convierte sus imágenes a texto Base64 y devuelve un JSON con id, nombre e imagen

def get_categories(request): #Define una función que Django usará como endpoint. request es la petición HTTP que llega del cliente (Android, navegador, ...)
    categories = Category.objects.all() #Solicita todas las filas de la tabla Category

    data = [] #Lista vacía de Python donde vamos a construir la respuesta JSON

    for cat in categories: #Recorre cada categoría de la base de datos
    
        data.append({
            "id": cat.id, #Id de la categoría
            "name": cat.name, #Nombre de la categoría
        })

    return JsonResponse(data, safe=False) #Devuelve la lista data como respuesta JSON HTTP
    #Con safe=False le indicamos que, aunque sea una lista en vez de un objeto, lo devuelva igualmente


def get_category_image(request, category_id):
    # Busca la categoría en la base de datos usando su ID
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    # Comprueba si la categoría tiene imagen
    if not category.image:
        return JsonResponse({"error": "No image"}, status=404)

    # Devuelve la imagen como respuesta HTTP
    return HttpResponse(category.image, content_type='image/jpeg')