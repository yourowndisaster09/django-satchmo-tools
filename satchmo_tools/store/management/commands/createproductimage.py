import os
import urllib

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.management.base import BaseCommand

from product.models import CategoryImage, ProductImage


class Command(BaseCommand):
    help = 'Uploads default unavailable product picture'

    def handle(self, *args, **options):
        try:
            product_image = ProductImage.objects.get(pk=1)
        except ProductImage.DoesNotExist:
            product_image = ProductImage()

        try:
            category_image = CategoryImage.objects.get(pk=1)
        except CategoryImage.DoesNotExist:
            category_image = CategoryImage()

        self._save_picture(product_image)
        self._save_picture(category_image)

        self.stdout.write('Added unavailable product picture\n')

    def _save_picture(self, image):
        file_path = finders.find(settings.DEFAULT_PRODUCT_IMAGE)
        result = urllib.urlretrieve(file_path)
        if hasattr(image, 'picture'):
            image.picture.delete()
        image.picture.save(
            os.path.basename(file_path),
            File(open(result[0]))
        )
        image.save()
