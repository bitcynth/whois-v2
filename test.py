from app.parsing.icann_parser import ICANNParser
from app.parsing import parse
from app import utils

with open('test/icann_format_data.txt') as f:
    icann_test_data = f.read()

#icann_parser = ICANNParser('as57782.net', icann_test_data)
#icann_parser.parse()
#print(icann_parser.get_data())
#print(parse('as57782.net', icann_test_data))
assert utils.get_resource_type('127.0.0.1') == 'ipv4', '127.0.0.1 is IPv4'
assert utils.get_resource_type('0.0.0.0') == 'ipv4', '0.0.0.0 is IPv4'
assert utils.get_resource_type('255.255.255.255') == 'ipv4', '255.255.255.255 is IPv4'
assert utils.get_resource_type('2a::') == 'ipv6', 'It is IPv6'
assert utils.get_resource_type('2a0d:1a45::') == 'ipv6', 'It is IPv6'
assert utils.get_resource_type('2a0d:1a45::1') == 'ipv6', 'It is IPv6'
assert utils.get_resource_type('aaaa:bbbb:cccc:dddd:eeee:ffff:0000:1111') == 'ipv6', 'It is IPv6'
assert utils.get_resource_type('cynthia.re') == 'domain', 'It is a domain'
assert utils.get_resource_type('nominet.org.uk') == 'domain', 'It is a domain'
assert utils.get_resource_type('nominet.uk') == 'domain', 'It is a domain'
assert utils.get_resource_type('iana.org') == 'domain', 'It is a domain'
assert utils.get_resource_type('cynthia') != 'domain', 'It is NOT a domain'