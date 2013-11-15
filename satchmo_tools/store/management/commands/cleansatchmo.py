from django.core.management.base import BaseCommand

from product.models import Product, Category
from product.modules.configurable.models import ConfigurableProduct
from satchmo_store.shop.models import Order, OrderItem, OrderPayment, Cart, CartItem


class Command(BaseCommand):
    help = 'Cleans store'

    def handle(self, *args, **options):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        OrderPayment.objects.all().delete()
        Cart.objects.all().delete()
        CartItem.objects.all().delete()
        Category.objects.all().delete()
        ConfigurableProduct.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write('Cleaned satchmo store\n')
