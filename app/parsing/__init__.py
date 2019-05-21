from app.parsing.icann_parser import ICANNParser
from app import config_data

def parse(obj, whois_data, qtype='domain'):
    if qtype == 'domain':
        whois_format = config_data.get_format_for_domain(obj)
        if whois_format == 'icann':
            icann_parser = ICANNParser(obj, whois_data)
            icann_parser.parse()
            return icann_parser.get_data()