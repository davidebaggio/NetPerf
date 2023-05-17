from managecmd import *
from fileout import *
import re
import socket
import calculation

'''# get rtt


def get_rtt(ping_out: str):
    rtt = get_lines(ping_out)[-1].split()[-2].split('/')
    if len(rtt) < 4:
        print("Error: No RTT found. Cannot read proper RTT, connection might be timed out")
        exit(1)
    return list(map(float, rtt))
'''
'''# get ttl


def get_ttl(ping_out: str):
    ttl = re.findall(r"ttl=(\d+)", ping_out)[1]
    if ttl is None:
        print("Error: No TTL found")
        exit(1)
    return int(ttl)
'''
# traceroute command


def traceroute(ip, sudo=False):
    if sudo:
        return run_command(['sudo', 'traceroute', ip])
    else:
        return run_command(['traceroute', ip])

# ping command


def ping(ip, n=1, ttl=64, size=64, sudo=False):
    if sudo:
        return run_command(['sudo', 'ping', '-c', str(n), '-t', str(ttl), '-s', str(size), ip])
    else:
        return run_command(['ping', '-c', str(n), '-t', str(ttl), '-s', str(size), ip])

# net performance


def run_netperf(ip: str, k_packets=10, l_packets=64, sudo=False, info=False):

    out = ping(ip, n=k_packets, size=l_packets, sudo=sudo)
    rtt = get_rtt(out)
    ttl = None

    if info:
        print(out)
        
        trace = traceroute(ip, sudo=sudo)
        ttl = get_ttl(out)
        
        print(trace)
        
        length = len(get_lines(trace)) - 1
        if length == 30:
            print("Max hops reached, Connection might be timed out")
            exit(1)
        # print(length)
        if (64 - ttl) == length:
            print("TTL is correct")
        print("RTT: ")
        print(rtt)
        output_to_file(ip, out)

    return rtt, ttl


def main():
    # sudo
    admin = input("Sudo (Y/N) ")
    if admin == "Y" or admin == "y":
        s = True
    elif admin == "N" or admin == "n":
        s = False
    else:
        print("Invalid input")
        exit()

    host = "lon.speedtest.clouvider.net"
    ip = get_ip(host)
    
    ttl = run_netperf(ip, l_packets=16, sudo=s, info=True)[1]
    hops = ttl * 2
    
    overall_performances = []
    steps = list(range(64, 1472, 64))
    for i in steps:
        print(f"Running netperf with packets of size {i * 8} bits")
        rtt = run_netperf(ip, l_packets=i, sudo=s)[0]
        overall_performances.append(rtt)
    
    # change steps from byte to all bit
    for i in range(len(steps)):
        steps[i] = (steps[i] + 28) * 8
    
    calculation.plot_all(steps, overall_performances)
    s, s_b = calculation.calculate_throughput(steps, overall_performances, hops)
    
    print(f"Throughput: {s} bits/s")
    print(f"Throughput Bottleneck: {s_b} bits/s")
