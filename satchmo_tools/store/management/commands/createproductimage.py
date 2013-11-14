import os
import urllib

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.management.base import BaseCommand

from product.models import ProductImage


class Command(BaseCommand):
    help = 'Uploads default unavailable product picture'

    def handle(self, *args, **options):
        image = ProductImage.objects.filter(product__isnull=True)
        file_path = finders.find(settings.DEFAULT_PRODUCT_IMAGE)
        result = urllib.urlretrieve(file_path)

        if image:
            product_image = image[0]
        else:
            product_image = ProductImage()

        product_image.picture.save(
            os.path.basename(file_path),
            File(open(result[0]))
        )
        product_image.save()
        self.stdout.write('Added unavailable product picture\n')
