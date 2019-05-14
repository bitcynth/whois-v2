from app.parsing.base_parser import BaseParser
import re

REGISTRANT_COUNTRY_CODE_REGEX = re.compile('^Registrant Country: ([A-Z][A-Z])')

REGEXES = {
    'registry_domain_id': '^Registry Domain ID: ([0-9A-Za-z_\-]+)',
    'registrar_whois': '^Registrar WHOIS Server: ([a-zA-Z0-9\-\.]+)',
    'registrar_url': '^Registrar URL: (.+)',
    'updated_date': '^Updated Date: ([TZ0-9\.\-:]+)',
    'creation_date': '^Creation Date: ([TZ0-9\.\-:]+)',
    'expiry_date': '^Registry Expiry Date: ([TZ0-9\.\-:]+)',
    'registrar_name': '^Registrar: (.+)',
    'registrar_iana_id': '^Registrar IANA ID: ([0-9]+)',
    'registrar_abuse_email': '^Registrar Abuse Contact Email: ([a-zA-Z@\.]+)',
    'registrar_abuse_phone': '^Registrar Abuse Contact Phone: (.+)',
    'domain_status': '^Domain Status: ([a-zA-Z]+) (https://icann.org/epp#[a-zA-Z]+)',
    'nameserver': '^Name Server: ([a-zA-Z\.\-_0-9]+)',
    'dnssec': '^DNSSEC: ([a-zA-Z]+)',
    'registrant_country': '^Registrant Country: ([A-Z][A-Z])'
}

class ICANNParser(BaseParser):
    def parse(self):
        tmp_data = {}
        for key, regex in REGEXES.items():
            reg = re.compile(regex, re.M)
            match = reg.findall(self.whois_data)
            if len(match) > 0:
                tmp_data[key] = match
        print(tmp_data)
        #self.data['registrar'] = {
        #    'iana_id': int(tmp_data['registrar_iana_id'])
        #}
        #self.data['registrant'] = {}