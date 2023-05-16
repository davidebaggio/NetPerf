from managecmd import *
from fileout import *
import os

# detect operating system
def detect_os():
	if os.name == "nt":
		return "windows"
	elif os.name == "posix":
		return "linux"
	else:
		return "unknown"

def run_netperf(ip, sudo=False):
	out = ping(ip, n=10, sudo=s)
	trace = traceroute(ip, sudo=s)
	return out, trace

os = detect_os()

if os == "linux":
	#sudo
	admin = input("Sudo (Y/N) ")
	if admin == "Y" or admin == "y":
		s = True
	elif admin == "N" or admin == "n":
		s = False
	else:
		print("Invalid input")
		exit()
else:
    s = False

ip = "atl.speedtest.clouvider.net"
netperf = run_netperf(ip, sudo=s)

rtt = list(map(float, get_rtt(netperf[0])))
ttl = get_ttl(netperf[0])
length = len(get_lines(netperf[1])) - 1

print("RTT: ")
print(rtt)

if (64 - ttl + 1) == length:
    print("TTL is correct")

output_to_file(ip, netperf[0], netperf[1], ttl)