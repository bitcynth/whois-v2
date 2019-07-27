import re

TYPE_IPV4_REGEX = re.compile('((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}')
TYPE_IPV6_REGEX = re.compile('^(?:[a-f0-9]{1,4}:){1,7}:?([a-f0-9]{1,4})?$')
TYPE_DOMAIN_REGEX = re.compile('^([a-z0-9-_]+\.)+([a-z0-9-_]+\.?)$')
TYPE_ASN_REGEX = re.compile('^as|AS([0-9]+)$')

def get_resource_type(res):
    if TYPE_DOMAIN_REGEX.match(res):
        return 'domain'
    if TYPE_IPV4_REGEX.match(res):
        return 'ipv4'
    if TYPE_IPV6_REGEX.match(res):
        return 'ipv6'
    if TYPE_ASN_REGEX.match(res):
        return 'asn'
    return 'other'