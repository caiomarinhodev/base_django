import importlib


from django.utils.functional import SimpleLazyObject
from django.contrib.sites.shortcuts import get_current_site
from django.conf import LazySettings


settings = LazySettings()


def site_name(request):
    site = SimpleLazyObject(lambda: get_current_site(request))
    protocol = 'https' if request.is_secure() else 'http'
    return {
        'site': site,
        'site_root': SimpleLazyObject(lambda: "{0}://{1}".format(protocol, site.domain)),
        'full_url': SimpleLazyObject(lambda: "{0}://{1}{2}".format(protocol, site.domain, request.path)),
        'path': SimpleLazyObject(lambda: "{0}".format(request.path)),
    }


def menus(request):
    return {
        "menus": filter(
            lambda x: x is not None,
            (get_menu_from_conf_file(app) for app in settings.INSTALLED_APPS)
        )
    }


def get_menu_from_conf_file(module_name):
    try:
        conf_module = importlib.import_module(f"{module_name}.conf")
        return conf_module.MENUS
    except (ModuleNotFoundError, AttributeError) as e:
        return
