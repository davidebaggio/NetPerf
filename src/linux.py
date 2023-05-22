from managecmd import *
from fileout import *
import pingparsing as pp

# print info
def print_info(ip: str, ping_info: str, rtt: list, TimeToLive: int, ttl: int):
    print(ping_info)
    print("------------------------------------")
    trace = traceroute(ip)
    print(f"TTL: {ttl}")
    print(trace)
    print("------------------------------------")
    length = len(get_lines(trace))
    if length == 30:
        print("Max hops reached, Connection might be timed out")
        exit(1)
    if (TimeToLive - ttl) == length:
        print("Route is correct")
    print(f"RTT: {rtt}")
    output_to_file(ip, ping_info)


# parsed stats
def parse_stats(ping_out: str):
    parser = pp.PingParsing()
    stats = parser.parse(ping_out)
    return stats


# get rtt
def get_rtt(ping_out: str):
    stats = parse_stats(ping_out)
    stats = stats.as_dict()
    rtt = []
    if stats['rtt_max'] is not None:
        rtt.append(stats['rtt_max'])
    if stats['rtt_min'] is not None:
        rtt.append(stats['rtt_min'])
    if stats['rtt_avg'] is not None:
        rtt.append(stats['rtt_avg'])
    if stats['rtt_mdev'] is not None:
        rtt.append(stats['rtt_mdev'])
    return rtt


# get ttl
def get_ttl(ping_out: str):
    stats = parse_stats(ping_out)
    ttl = stats.icmp_replies[0]['ttl']
    return int(ttl)


# traceroute command
def traceroute(ip, sudo=False):
    if sudo:
        return run_command(['sudo', 'traceroute', ip])
    else:
        return run_command(['traceroute', ip])


# ping command
def ping(ip, n, ttl, size, sudo):
    if sudo:
        return run_command(['sudo', 'ping', '-c', str(n), '-t', str(ttl), '-s', str(size), ip])
    else:
        return run_command(['ping', '-c', str(n), '-t', str(ttl), '-s', str(size), ip])

# net performance
def run_netperf(ip: str, k_packets=10, TimeToLive=64, l_packets=64, sudo=False, info=False):

    ping_info = ping(ip, n=k_packets, ttl=TimeToLive, size=l_packets, sudo=sudo)
    rtt = get_rtt(ping_info)
    ttl = get_ttl(ping_info)

    if info:
        print_info(ip, ping_info, rtt, TimeToLive, ttl)

    return rtt, ttl


def main(ip: str, steps: list):
    # sudo
    admin = input("Sudo (Y/N) ")
    if admin == "Y" or admin == "y":
        s = True
    elif admin == "N" or admin == "n":
        s = False
    else:
        print("Invalid input")
        exit()

    ttl = run_netperf(ip, l_packets=16, sudo=s, info=True)[1]
    actual_hops = ttl * 2
    print(f"Number of links crossed: {actual_hops}")
    
    overall_performances = []
    for i in steps:
        print("++++++++++++++++++++++++++++++++++++++++++++")
        print(f"Running netperf with packets of size {i * 8} bits")
        rtt = run_netperf(ip, l_packets=i, sudo=s)[0]
        overall_performances.append(rtt)

    return overall_performances, actual_hops
