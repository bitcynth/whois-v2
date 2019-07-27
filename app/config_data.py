import re
import os

WHOIS_SERVER_REGEX = re.compile('^([a-zA-Z0-9_\-]+)\s+([a-zA-Z0-9\-\.]+)')
ASNS_REGEX = re.compile('^([0-9]+)\-([0-9]+)\s+([a-zA-Z0-9_\-\.]+)')
INDIVIDUAL_ASN_REGEX = re.compile('^([0-9]+)\s+([a-zA-Z0-9_\-\.]+)')
DOMAINS_REGEX = re.compile('^([a-zA-Z0-9\.\-]+)\s+([a-zA-Z0-9_\-\.]+)\s+([a-zA-Z0-9_\-]+)')
OTHERS_REGEX = re.compile('^(.*)\s+([a-zA-Z0-9_\-\.]+)')
COMMENTS_REGEX = re.compile('#.*')

whois_servers = {}
domains = {}
asns = {}
others = []

class DomainEntry(object):
    def __init__(self, server, format):
        self.server = server
        self.format = format

class OtherEntry(object):
    def __init__(self, regex, server):
        self.server = server
        self.regex = re.compile(regex)

def load_data(asns_file='data/asns.txt', domains_file='data/domains.txt', whois_servers_file='data/whois_servers.txt', others_file='data/other.txt'):
    this_dir, this_filename = os.path.split(__file__)

    with open(os.path.join(this_dir, whois_servers_file)) as f:
        for line in f.readlines():
            line = COMMENTS_REGEX.sub('', line)
            if line == '':
                continue
            match = WHOIS_SERVER_REGEX.findall(line)
            if len(match) > 0 and len(match[0]) > 1:
                whois_servers[match[0][0]] = match[0][1]
    with open(os.path.join(this_dir, asns_file)) as f:
        for line in f.readlines():
            line = COMMENTS_REGEX.sub('', line)
            if line == '':
                continue
            match = INDIVIDUAL_ASN_REGEX.findall(line)
            if len(match) > 0 and len(match[0]) > 1:
                asns[match[0][0]] = match[0][1]
            match = ASNS_REGEX.findall(line)
            if len(match) > 0 and len(match[0]) > 2:
                asns[match[0][0]+'-'+match[0][1]] = match[0][2]
                pass
    with open(os.path.join(this_dir, domains_file)) as f:
        for line in f.readlines():
            line = COMMENTS_REGEX.sub('', line)
            if line == '':
                continue
            match = DOMAINS_REGEX.findall(line)
            if len(match) > 0 and len(match[0]) > 1:
                domains[match[0][0]] = DomainEntry(match[0][1], match[0][2])
    with open(os.path.join(this_dir, others_file)) as f:
        for line in f.readlines():
            line = COMMENTS_REGEX.sub('', line)
            if line == '':
                continue
            match = OTHERS_REGEX.findall(line)
            if len(match) > 0 and len(match[0]) > 1:
                o = OtherEntry(match[0][0], match[0][1])
                others.append(o)

def get_server_for_domain(domain):
    parts = domain.split('.')
    for i, d in enumerate(parts):
        dom = '.'.join(parts[i:])
        if dom in domains:
            print(domain)
            if domains[d].server in whois_servers:
                return whois_servers[domains[d].server]
            return domains[d].server

def get_server_for_other(other):
    for o in others:
        match = o.regex.findall(other.lower())
        if len(match) > 0:
            if o.server in whois_servers:
                return whois_servers[o.server]
            return o.server

def get_server_for_asn(asn):
    asn = asn.replace('AS', '').replace('as', '')
    if asn in asns:
        if asns[asn] in whois_servers:
            return whois_servers[asns[asn]]
        return asns[asn]
    for a in asns:
        parts = a.split('-')
        if len(parts) < 2:
            continue
        first = int(parts[0])
        last = int(parts[1])
        asn_int = int(asn)
        if asn_int >= first and asn_int <= last:
            if asns[a] in whois_servers:
                return whois_servers[asns[a]]
            return asns[a]
    return None

def get_format_for_domain(domain):
    parts = domain.split('.')
    for i, d in enumerate(parts):
        dom = '.'.join(parts[i:])
        if dom in domains:
            return domains[d].format