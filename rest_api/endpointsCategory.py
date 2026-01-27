import base64 #Importa una librería de Python que sirve para convertir datos binarios (bytes) en texto (Base64)
              #La necesitamos porque cat.image es binario y JSON no puede enviar binarios
from django.http import JsonResponse, \
    HttpResponse  # Importa la clase que permite devolver respuestas HTTP en formato JSON desde Django
from .models import Category #Importa el modelo Category para poder leer las categorías de la base de datos


#Esta función lee todas las categorías de la BD, convierte sus imágenes a texto Base64 y devuelve un JSON con id, nombre e imagen

def get_categories(request): #Define una función que Django usará como endpoint. request es la petición HTTP que llega del cliente (Android, navegador, ...)
    categories = Category.objects.all() #Solicita todas las filas de la tabla Category

    data = [] #Lista vacía de Python donde vamos a construir la respuesta JSON

    for cat in categories: #Recorre cada categoría de la base de datos
        image_base64 = None #Por defecto indicamos que la categoría no tiene imagen
        if cat.image: #Si tiene imagen:
            image_base64 = base64.b64encode(cat.image).decode("utf-8")
            #cat.image --> son bytes (binario)
            #base64.b64encode --> convierte esos bytes en Base64
            #decode("utf-8") --> convierte eso en texto normal (string)
            #Como resultado obtenemos una cadena de texto que se puede enviar en JSON

        data.append({ #Añadimos un nuevo elemento a la lista "data"
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
        # Si no existe, devuelve un error 404 en formato JSON
        return JsonResponse({"error": "Not found"}, status=404)

    # Comprueba si la categoría tiene imagen
    if not category.image:
        # Si no tiene imagen, devuelve otro error 404
        return JsonResponse({"error": "No image"}, status=404)


    # Devuelve la imagen como respuesta HTTP
    return HttpResponse(category.image, content_type='image/jpeg')



