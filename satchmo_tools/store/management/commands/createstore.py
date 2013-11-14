from optparse import make_option

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError

from l10n.models import Country
from satchmo_store.shop.models import Config


class Command(BaseCommand):
    help = 'Creates Store Configuration'
    base_options = (
        make_option('--override', action='store_true', dest='override', default=False,
            help='Override existing store configuration'
        ),
    )
    option_list = BaseCommand.option_list + base_options

    def __init__(self):
        super(Command, self).__init__()
        self.set_settings()
        self.site = self.create_site_object()

    def handle(self, *args, **options):
        create_new = False
        try:
            Config.objects.get(site=self.site)
        except Config.DoesNotExist:
            create_new = True
            print("No existing configuration")

        if options.get('override'):
            create_new = True
            print("Overriding existing store configuration")

        if create_new:
            self.create_store_config()
            self.stdout.write('Completed creating store configuration\n')
        else:
            self.stdout.write('Already has store configuration\n')

    def _set_settings(self, name):
        try:
            setting_value = getattr(settings, name)
            setattr(self, name, setting_value)
        except AttributeError:
            raise CommandError('Add `%s` to settings' % name)

    def set_settings(self):
        required_settings = [
            'ENV_SITE_NAME',
            'SHOP_NAME',
            'COUNTRY_NAME'
        ]
        for s in required_settings:
            self._set_settings(s)

    def create_site_object(self):
        try:
            site = Site.objects.get(pk=1)
            site.name = self.SHOP_NAME
            site.domain = self.ENV_SITE_NAME
            site.save()
            return site
        except Site.DoesNotExist:
            return Site.objects.create(
                name=self.SHOP_NAME,
                domain=self.ENV_SITE_NAME
            )

    def create_store_config(self):
        try:
            country = Country.objects.get(name=self.COUNTRY_NAME)
        except Country.DoesNotExist:
            raise CommandError('You must run `python manage.py satchmo_load_l10n`\
                first or enter a valid country')

        try:
            config = Config.objects.get(site=self.site)
            config.store_name = self.SHOP_NAME
            config.country = country
            config.sales_country = country
            config.save()
        except Config.DoesNotExist:
            config = Config.objects.create(
                site=self.site,
                store_name=self.SHOP_NAME,
                country=country,
                sales_country=country
            )
        config.shipping_countries.add(country)
