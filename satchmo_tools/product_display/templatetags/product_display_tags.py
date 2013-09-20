from django.template import Library

from product.models import Product
from product.queries import bestsellers


register = Library()


@register.assignment_tag
def random_featured(n):
    products = Product.objects.active_by_site()
    products = products.filter(featured=True)
    return products.order_by('?')[:n]


@register.assignment_tag
def bestsellers(n):
    return bestsellers(n)


@register.assignment_tag
def recently_added(n):
    return Product.objects.recent_by_site()[:n]


@register.assignment_tag
def random_products(n):
    products = Product.objects.active_by_site()
    return products.order_by('?')[:n]
