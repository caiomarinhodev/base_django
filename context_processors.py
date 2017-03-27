from django.utils.functional import SimpleLazyObject
from django.contrib.sites.shortcuts import get_current_site


def site_name(request):
    site = SimpleLazyObject(lambda: get_current_site(request))
    protocol = 'https' if request.is_secure() else 'http'
    print site
    return {
        'site': site,
        'site_root': SimpleLazyObject(lambda: "{0}://{1}".format(protocol, site.domain)),
        'full_url': SimpleLazyObject(lambda: "{0}://{1}{2}".format(protocol, site.domain, request.path)),
        'path': SimpleLazyObject(lambda: "{0}".format(request.path)),
    }