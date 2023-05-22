from managecmd import *
from fileout import *
import re
import statistics
import calculation

# print info
def print_info(ip: str, ping_info: str, rtt: list, TimeToLive: int, ttl: int):
    print(ping_info)
    print("------------------------------------")
    
    trace = tracert(ip)
    print(f"TTL: {ttl}")
    
    print(trace)
    print("------------------------------------")

    length = len(get_lines(trace)) - 4
    if length == 30:
        print("Max hops reached, Connection might be timed out")
        exit(1)
    
    if (TimeToLive - ttl) == length:
        print("Route is correct")
    print(f"RTT: {rtt}")
    output_to_file(ip, ping_info)

# get rtt
def get_rtt(ping_out: str):
    rttLine = get_lines(ping_out)[-1].split(',')
    rtt = []
    for l in rttLine:
        rtt.append(l.split('=')[1].split()[-1][:-2])
    rtt[1], rtt[2] = rtt[2], rtt[1]
    return list(map(float, rtt))

# get ttl
def get_ttl(ping_out: str):
    return int(re.findall(r"TTL=(\d+)", ping_out)[1])


# tracert command
def tracert(ip):
    return run_command(['tracert', ip])


# ping command
def ping(ip, n, ttl, size):
    return run_command(['ping', '-n', str(n), '-i', str(ttl), '-l', str(size), ip])


# get stdev
def get_stdev(out: str):
    round_trip_times = re.findall(r"=(\d+)ms", out)
    round_trip_times = list(map(int, round_trip_times))
    stdev = statistics.pstdev(round_trip_times)
    return stdev


# net performance
def run_netperf(ip: str, k_packets=10, TimeToLive=64, l_packets=64, info=False):
    ping_info = ping(ip, n=k_packets, ttl=TimeToLive, size=l_packets)
    rtt = get_rtt(ping_info)
    rtt.append(get_stdev(ping_info))
    ttl = get_ttl(ping_info)

    if info:
        print_info(ip, ping_info, rtt, TimeToLive, ttl)

    return rtt, ttl


def main(ip: str, steps: list):
    ttl = run_netperf(ip, l_packets=4, info=True)[1]
    actual_hops = ttl * 2
    print(f"Number of links crossed: {actual_hops}")
    
    overall_performances = []
    
    for i in steps:
        print("++++++++++++++++++++++++++++++++++++++++++++")
        print(f"Running netperf with packets of size {i * 8} bits")
        rtt = run_netperf(ip, l_packets=i)[0]
        overall_performances.append(rtt)

    return overall_performances, actual_hops
