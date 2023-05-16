from managecmd import *
from fileout import *
import re
import statistics
import socket

# get rtt


def get_rtt(ping_out: str):
    rttLine = get_lines(ping_out)[-1].split(',')
    rtt = []
    for l in rttLine:
        rtt.append(l.split('=')[1].split()[-1][:-2])
    return list(map(float, rtt))

# get ttl


def get_ttl(ping_out: str):
    return re.findall(r"TTL=(\d+)", ping_out)[1]


# tracert command


def tracert(ip):
    return run_command(['tracert', ip])

# get ip


def get_ip(url):
    ip = socket.gethostbyname(url)
    return ip

# ping command


def ping(ip, n=1, ttl=64, size=64):
    return run_command(['ping', '-n', str(n), '-i', str(ttl), '-l', str(size), ip])

# net performance


def run_netperf(ip: str, k_packets=10, l_packets=64, info=False):

    out = ping(ip, n=k_packets, size=l_packets)

    rtt = get_rtt(out)
    round_trip_times = re.findall(r"=(\d+)ms", out)
    round_trip_times = list(map(int, round_trip_times))
    # print(round_trip_times)
    stdev = statistics.pstdev(round_trip_times)
    rtt.append(stdev)

    if info:
        print(out)
        ttl = get_ttl(out)
        print(ttl)

        trace = tracert(ip)
        print(trace)

        length = len(get_lines(trace))
        print(length)
        if (64 - ttl + 1) == length:
            print("TTL is correct")
        output_to_file(ip, out, trace, ttl)

    return rtt


def main():
    host = "atl.speedtest.clouvider.net"
    ip = get_ip(host)
    print(ip)
    run_netperf(ip, l_packets=10, info=True)

    overall_performances = []
    steps = list(range(64, 1472, 64))

    '''for i in steps:
		print("-----------------------")
		print(f"Running netperf with packets of size {i * 8} bits")
		overall_performances.append(run_netperf(ip, l_packets=i))
'''