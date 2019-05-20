import re

WHOIS_SERVER_REGEX = re.compile('^([a-zA-Z0-9_\-]+)\s+([a-zA-Z0-9\-\.]+)')
ASNS_REGEX = re.compile('^([0-9]+)\-([0-9]+)\s+([a-zA-Z0-9_\-]+)')
DOMAINS_REGEX = re.compile('^([a-zA-Z0-9\.\-]+)\s+([a-zA-Z0-9_\-]+)')

whois_servers = {}
domains = {}
asns = {}

def load_data(asns_file='data/asns.txt', domains_file='data/domains.txt', whois_servers_file='data/whois_servers.txt'):
    with open(whois_servers_file) as f:
        for line in f.readlines():
            match = WHOIS_SERVER_REGEX.findall(line)
            if len(match) > 0 and len(match[0]) > 1:
                whois_servers[match[0][0]] = match[0][1]
    with open(asns_file) as f:
        for line in f.readlines():
            match = ASNS_REGEX.findall(line)
            if len(match) > 0 and len(match[0]) > 2:
                # TODO: ASN lists
                #asns[match[0][0]] = match[0][1]
                pass
    with open(domains_file) as f:
        for line in f.readlines():
            match = DOMAINS_REGEX.findall(line)
            if len(match) > 0 and len(match[0]) > 1:
                domains[match[0][0]] = match[0][1]

def get_server_for_domain(domain):
    parts = domain.split('.')
    for i, d in enumerate(parts):
        dom = '.'.join(parts[i:])
        if dom in domains:
            return whois_servers[domains[d]]
        