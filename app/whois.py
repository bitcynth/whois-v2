import socket
import re

from app import config_data, utils

BUFFER_SIZE = 4096

IANA_WHOIS_REFER_REGEX = re.compile('whois:[\s]+([\.a-z0-9\-]+)')

def whois_raw(server, query, port=43, encoding=None):
    if encoding is None:
        # try to find the correct encoding if not provided
        encoding = config_data.get_encoding_for_server(server)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((server, port))
    s.send('{}\r\n'.format(query).encode(encoding))
    result = ''
    tmp = b''
    while True:
        tmp = s.recv(BUFFER_SIZE)
        result += tmp.decode(encoding, errors='replace')
        if len(tmp) == 0:
            break
    return result

def query_via_root(query):
    root_res = whois_raw('whois.iana.org', query)
    m = IANA_WHOIS_REFER_REGEX.findall(root_res)
    if len(m) == 0:
        return root_res
    server = m[0]
    whois_res = whois_raw(server, query)
    return whois_res

def query_via_list(query, qtype=None):
    res = 'error'
    if qtype == None:
        qtype = utils.get_resource_type(query)
    if qtype == 'domain':
        server = config_data.get_server_for_domain(query)
        if server is None:
            return query_via_root(query)
        res = whois_raw(server, query)
    elif qtype == 'asn':
        server = config_data.get_server_for_asn(query)
        if server is None:
            return query_via_root(query)
        res = whois_raw(server, query)
    elif qtype == 'other':
        server = config_data.get_server_for_other(query)
        if server is None:
            return query_via_root(query)
        res = whois_raw(server, query)
    else:
        return query_via_root(query)
    return res

def query_whois(query, flags=[]):
    if 'no_list' in flags:
        return query_via_root(query)
    return query_via_list(query)