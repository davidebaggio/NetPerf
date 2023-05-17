import pingparsing as pp
from fileout import *
from managecmd import *
import socket
import json

def get_ip(host):
    return socket.gethostbyname(host)


n = 10
ttl = 64
size = 56
host = "lon.speedtest.clouvider.net"
ip = get_ip(host)
output = run_command(['ping', '-c', str(n), '-t', str(ttl), '-s', str(size), ip])

output_to_file(host, output)

parser = pp.PingParsing()
stats = parser.parse(output)
print(type(stats.as_dict()['rtt_max']))
print(json.dumps(stats.as_dict(), indent=4))

print(stats.icmp_replies[0]['ttl'])
#for icmp in stats.icmp_replies:
#    print(icmp['ttl'])
