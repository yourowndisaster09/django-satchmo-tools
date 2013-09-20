from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError

from l10n.models import Country
from satchmo_store.shop.models import Config


class Command(BaseCommand):
    help = 'Creates Jajomaxx Store Configuration'

    def __init__(self):
        super(Command, self).__init__()
        self.check_settings()
        self.site = self.create_site_object()

    def handle(self, *args, **options):
        self.create_store_config()
        self.stdout.write('Completed creating Jajomaxx store configuration\n')

    def check_settings(self):
        try:
            self.ENV_SITE_NAME = settings.ENV_SITE_NAME
        except AttributeError:
            raise CommandError('Add `ENV_SITE_NAME` to settings')

        try:
            self.SHOP_NAME = settings.SHOP_NAME
        except AttributeError:
            raise CommandError('Add `SHOP_NAME` to settings')

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
            usa_country = Country.objects.get(name="UNITED STATES")
        except Country.DoesNotExist:
            raise CommandError('Run `python manage.py satchmo_load_l10n` first')

        try:
            config = Config.objects.get(site=self.site)
            config.store_name = "Jajomaxx"
            config.country = usa_country
            config.sales_country = usa_country
            config.save()
        except Config.DoesNotExist:
            config = Config.objects.create(
                site=self.site,
                store_name="Jajomaxx",
                country=usa_country,
                sales_country=usa_country
            )
        config.shipping_countries.add(usa_country)
