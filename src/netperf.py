from managecmd import *
from fileout import *
import os
import numpy as np
import matplotlib.pyplot as plt


# detect operating system
def detect_os():
	if os.name == "nt":
		return "windows"
	elif os.name == "posix":
		return "linux"
	else:
		return "unknown"

# running network performance
def run_netperf(ip: str, k_packets=10, l_packets=64, sudo=False, info=False):
	out = ping(ip, n=k_packets, size=l_packets, sudo=s)
	trace = traceroute(ip, sudo=s)

	print(out)
	
	rtt = get_rtt(out)
	ttl = get_ttl(out)
	length = len(get_lines(trace)) - 1


	if (64 - ttl + 1) == length:
		print("TTL is correct")
	if info:
		print("RTT: ")
		print(rtt)
		output_to_file(ip, out, trace, ttl)
	return rtt


if __name__ == "__main__":
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
	run_netperf(ip, l_packets=10, sudo=s, info=True)

	overall_performances = []
	steps = list(range(64, 1472, 64))

	for i in steps:
		print("-----------------------")
		print(f"Running netperf with packets of size {i * 8} bits")
		overall_performances.append(run_netperf(ip, l_packets=i, sudo=s))

