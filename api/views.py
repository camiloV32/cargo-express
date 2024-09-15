from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import jwt
import json
import datetime

from .models import Delivery, Order, Product, User, OrderProduct
from django.contrib.auth.hashers import make_password, check_password

# Genera un token JWT para un repartidor si el IdRepartidor proporcionado es válido
@csrf_exempt
def generate_token_delivery(request):
    if request.method == 'POST':
        # Cargar los datos del cuerpo de la solicitud
        data = json.loads(request.body)

        # Validar datos
        if not isinstance(data.get('IdRepartidor'), int):
            return JsonResponse({'message': 'El campo IdRepartidor debe ser un número entero'}, status=400)

        # Establecer el tiempo de expiración del token (1 minuto a partir de ahora)
        data['exp'] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10)
        
        # Verificar si existe un repartidor con el IdRepartidor proporcionado
        if Delivery.objects.filter(id=data['IdRepartidor']).exists():
            # Generar el token JWT
            token = jwt.encode(data, settings.SECRET_KEY, algorithm='HS256')
            return JsonResponse({'token': token, 'message': 'Ok'})
        else:
            # Retornar un error si el repartidor no existe
            return JsonResponse({'message': 'No eres un repartidor'}, status=401)


from django.db import transaction
from django.http import JsonResponse
import json
import jwt
from django.conf import settings
from .models import Delivery, Order, OrderProduct, Product

@csrf_exempt
def register_order(request):
    if request.method == 'POST':
        # Obtener token de la cabecera Authorization
        token = request.headers.get('Authorization')

        # Obtener y validar datos del payload
        data = json.loads(request.body)

        if not isinstance(data['pedido_id'], str):
            return JsonResponse({'message': 'El campo pedido_id debe ser una cadena de texto'})
        if not isinstance(data['timestamp'], str):
            return JsonResponse({'message': 'El campo timestamp debe ser una cadena de texto'})
        if not isinstance(data['repartidor']['IdRepartidor'], int):
            return JsonResponse({'message': 'El campo IdRepartidor debe ser un número entero'})

        # Verificar si el token es válido
        try:
            decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'El token ha expirado'})
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Token inválido'})

        
        # Obtener y validar el repartidor
        delivery = get_delivery(data['repartidor']['IdRepartidor'])
        if not delivery:
            return JsonResponse({'message': 'Repartidor no encontrado'}, status=404)

        if not decode_token['IdRepartidor'] == delivery.id:
            return JsonResponse({'message': 'Este token no te pertenece'}, status=401)
        # Usar transacciones para manejar la creación de la orden y los productos
        try:
            with transaction.atomic():
                # Crear pedido
                order = create_order(data, delivery)
                if not order:
                    return JsonResponse({'message': 'Error al crear la orden'}, status=500)

                # Crear productos en tabla OrderProduct
                products = create_order_products(data['productos'], order)

                # Retornar con status 201 (created)
                return JsonResponse({
                    'message': 'Create',
                    'id_orden': order.id,
                    'products': products
                }, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Error al procesar el pedido'}, status=500)

# Función para obtener y validar repartidor
def get_delivery(delivery_id):
    try:
        return Delivery.objects.get(id=delivery_id)
    except Delivery.DoesNotExist:
        return None

# Función que crea el pedido
def create_order(data, delivery):
    try:
        order = Order.objects.create(
            order_code=data['pedido_id'],
            delivery=delivery,
            timestamp=data['timestamp']
        )
        return order
    except Exception as e:
        print(e)
        return None

# Función para agregar productos a un pedido, combinando duplicados y registrando la cantidad de cada producto en la base de datos
def create_order_products(products, order):
    # Unimos los productos duplicados y agregamos la cantidad de veces que está en la lista
    product_counts = {}
    for product in products:
        product_id = product['IdProducto']
        product_counts[product_id] = product_counts.get(product_id, {**product, 'quantity': 0})
        product_counts[product_id]['quantity'] += 1
    # Obtenemos el id de cada producto y buscamos si existen estos ids en la base de datos
    product_ids = list(product_counts.keys())
    existing_products = Product.objects.filter(id__in=product_ids)
    # Guardamos cada orden-producto
    for product in existing_products:
        quantity = product_counts[str(product.id)]['quantity']
        OrderProduct.objects.create(order=order, product=product, quantity=quantity)

    return product_counts


