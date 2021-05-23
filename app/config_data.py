import re
import os

WHOIS_SERVER_REGEX = re.compile('^([a-zA-Z0-9_\-]+)\s+([a-zA-Z0-9\-\.]+)')
ASNS_REGEX = re.compile('^([0-9]+)\-([0-9]+)\s+([a-zA-Z0-9_\-\.]+)')
INDIVIDUAL_ASN_REGEX = re.compile('^([0-9]+)\s+([a-zA-Z0-9_\-\.]+)')
DOMAINS_REGEX = re.compile('^([a-zA-Z0-9\.\-]+)\s+([a-zA-Z0-9_\-\.]+)\s+([a-zA-Z0-9_\-]+)')
OTHERS_REGEX = re.compile('^(.*)\s+([a-zA-Z0-9_\-\.]+)')
ENCODING_REGEX = re.compile('^([a-zA-Z0-9_\-]+)\s+([a-zA-Z0-9_\-\.]+)')
COMMENTS_REGEX = re.compile('#.*')

whois_servers = {}
whois_server_labels = {}
domains = {}
asns = {}
others = []
server_encodings = {}

class DomainEntry(object):
    def __init__(self, server, format):
        self.server = server
        self.format = format

class OtherEntry(object):
    def __init__(self, regex, server):
        self.server = server
        self.regex = re.compile(regex)

def load_data(asns_file='data/asns.txt', domains_file='data/domains.txt', whois_servers_file='data/whois_servers.txt', others_file='data/other.txt', encodings_file='data/encodings.txt'):
    this_dir, this_filename = os.path.split(__file__)

    with open(os.path.join(this_dir, whois_servers_file)) as f:
        for line in f.readlines():
            line = COMMENTS_REGEX.sub('', line)
            if line == '':
                continue
            match = WHOIS_SERVER_REGEX.findall(line)
            if len(match) > 0 and len(match[0]) > 1:
                server_label = match[0][0]
                server_addr = match[0][1]
                whois_servers[server_label] = server_addr
                whois_server_labels[server_addr] = server_label
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
    with open(os.path.join(this_dir, encodings_file)) as f:
        for line in f.readlines():
            line = COMMENTS_REGEX.sub('', line)
            if line == '':
                continue
            match = ENCODING_REGEX.findall(line)
            if len(match) > 0 and len(match[0]) > 1:
                server_encodings[match[0][0]] = match[0][1]

def get_server_for_domain(domain):
    parts = domain.split('.')
    for i, d in enumerate(parts):
        dom = '.'.join(parts[i:])
        if dom in domains:
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

def get_encoding_for_server(server_address):
    if not server_address in whois_server_labels:
        return server_encodings['DEFAULT']
    server_label = whois_server_labels[server_address]
    if not server_label in server_encodings:
        return server_encodings['DEFAULT']
    return server_encodings[server_label]
