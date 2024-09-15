import json
from django.db.models import Count, Sum, F, FloatField, ExpressionWrapper
from api.models import OrderProduct, Order

def get_sales_metrics():
    # Producto más vendido
    most_sold_product = OrderProduct.objects.values('product__name') \
        .annotate(total_quantity_sold=Sum('quantity')) \
        .order_by('-total_quantity_sold').first()
    
    if most_sold_product is None:
        most_sold_product = {'product__name': 'N/A', 'total_quantity_sold': 0}

    # Total de ventas por producto
    total_sales_per_product = OrderProduct.objects.values('product__name') \
        .annotate(total_quantity_sold=Sum('quantity')) \
        .order_by('-total_quantity_sold')
    
    # Ingresos totales por producto
    total_revenue_per_product = OrderProduct.objects.values('product__name') \
        .annotate(total_revenue=Sum(
            ExpressionWrapper(F('quantity') * F('product__price'), output_field=FloatField())
        )) \
        .order_by('-total_revenue')

    # Delivery con más pedidos
    top_delivery = Order.objects.values('delivery__user_id__name') \
        .annotate(total_orders=Count('id')) \
        .order_by('-total_orders') \
        .first()
    
    if top_delivery is None:
        top_delivery = {'delivery__user_id__name': 'N/A', 'total_orders': 0}

    # Construir el resultado en formato JSON
    metrics = {
        'most_sold_product': {
            'product_name': most_sold_product['product__name'],
            'total_quantity_sold': most_sold_product['total_quantity_sold'],
        },
        'total_sales_per_product': [
            {
                'product_name': product['product__name'],
                'total_quantity_sold': product['total_quantity_sold'],
            } for product in total_sales_per_product
        ],
        'total_revenue_per_product': [
            {
                'product_name': product['product__name'],
                'total_revenue': product['total_revenue'],
            } for product in total_revenue_per_product
        ],
        'top_delivery': {
            'delivery_name': top_delivery['delivery__user_id__name'],
            'total_orders': top_delivery['total_orders'],
        }
    }

    return json.dumps(metrics, indent=4)
