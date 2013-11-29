import urllib
from optparse import make_option

from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from ....config import get_satchmo_tools_setting


class Command(BaseCommand):
    help = 'Uploads default unavailable product picture'
    base_options = (
        make_option('--override', action='store_true', dest='override', default=False,
            help='Override existing unavailable product picture'
        ),
    )
    option_list = BaseCommand.option_list + base_options

    def handle(self, *args, **options):
        product_image = get_satchmo_tools_setting('DEFAULT_PRODUCT_IMAGE')
        file_path = finders.find(product_image)

        result = urllib.urlretrieve(file_path)
        content = File(open(result[0]))

        filenames = [
            'images/productimage-picture-default.jpg',
            'images/categoryimage-picture-default.jpg'
        ]

        for filename in filenames:
            if not default_storage.exists(filename):
                default_storage.save(filename, content)
            elif options.get('override'):
                default_storage.delete(filename)
                default_storage.save(filename, content)