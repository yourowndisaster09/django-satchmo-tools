from django.conf import settings


satchmo_tools_settings_defaults = {
    'SHOP_NAME' : None,
    'COUNTRY_NAME' : None,
    'POSTAL_CODE' : None,
    'DEFAULT_PRODUCT_IMAGE' : None,
    'IS_INTERNATIONAL' : False
}

def get_satchmo_tools_setting(name, default_value = None):
    if not hasattr(settings, 'SATCHMO_TOOLS_SETTINGS'):
        return satchmo_tools_settings_defaults.get(name, default_value)

    return settings.SATCHMO_TOOLS_SETTINGS.get(name, satchmo_tools_settings_defaults.get(name, default_value))
