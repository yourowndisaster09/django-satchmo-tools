import os
import urllib

from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.management.base import BaseCommand

from product.models import CategoryImage, ProductImage

from ....config import get_satchmo_tools_setting


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
        product_image = get_satchmo_tools_setting('DEFAULT_PRODUCT_IMAGE')
        file_path = finders.find(product_image)
        result = urllib.urlretrieve(file_path)
        if hasattr(image, 'picture') and image.picture:
            image.picture.delete()
        image.picture.save(
            os.path.basename(file_path),
            File(open(result[0]))
        )
        image.save()
