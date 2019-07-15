import socket
import re

from app import config_data

BUFFER_SIZE = 4096

IANA_WHOIS_REFER_REGEX = re.compile('whois:[\s]+([\.a-z0-9\-]+)')

def whois_raw(server, query, port=43):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((server, port))
    s.send('{}\r\n'.format(query).encode('utf-8'))
    result = ''
    tmp = b''
    while True:
        tmp = s.recv(BUFFER_SIZE)
        result += tmp.decode('utf-8')
        if len(tmp) == 0:
            break
    return result

def query_via_root(query):
    root_res = whois_raw('whois.iana.org', query)
    m = IANA_WHOIS_REFER_REGEX.findall(root_res)
    if m == 0:
        return root_res
    server = m[0]
    whois_res = whois_raw(server, query)
    return whois_res

def query_via_list(query, qtype='domain'):
    res = 'error'
    if qtype == 'domain':
        server = config_data.get_server_for_domain(query)
        res = whois_raw(server, query)
    return res

def query_whois(query, flags=[]):
    if 'no_list' in flags:
        return query_via_root(query)
    return query_via_list(query)