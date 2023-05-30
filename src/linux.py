from managecmd import *
from fileout import *
import pingparsing as pp

# print route info


def route_info(ip: str, sudo):
    print("-------------Finding amount of hops to the host-------------")
    count_hops = 64
    while count_hops > 0:
        try:
            ping(ip, n=1, ttl=count_hops, size=1, sudo=sudo)
            count_hops -= 1
        except Exception:
            count_hops += 1
            break
    print("------------------------------------------------------------")
    if count_hops == 0:
        print("No links found, connection might be timed out")
        exit(1)

    ping_info = ping(ip, n=10, ttl=64, size=64, sudo=sudo)
    print(ping_info)
    print("------------------------------------")
    trace = traceroute(ip)
    print(trace)
    print("------------------------------------")
    length = len(get_lines(trace)) - 1
    if length == 30:
        print("Max hops reached, Connection might be timed out")
        exit(1)
    if count_hops == length:
        print("Route is correct")
    print(f"Hops to host: {count_hops}")
    output_to_file(ip, ping_info)

    return count_hops


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
    if stats['rtt_min'] != None:
        rtt.append(stats['rtt_min'])
    if stats['rtt_avg'] != None:
        rtt.append(stats['rtt_avg'])
    if stats['rtt_max'] != None:
        rtt.append(stats['rtt_max'])
    if stats['rtt_mdev'] != None:
        rtt.append(stats['rtt_mdev'])
    return rtt


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


def run_netperf(ip: str, k_packets=20, TimeToLive=64, l_packets=64, sudo=False):

    ping_info = ping(ip, n=k_packets, ttl=TimeToLive,
                     size=l_packets, sudo=sudo)
    rtt = get_rtt(ping_info)

    return rtt


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

    hops = route_info(ip, sudo=s)
    actual_hops = hops * 2
    print(f"Number of links crossed: {actual_hops}")

    overall_performances = []
    for i in steps:
        print("++++++++++++++++++++++++++++++++++++++++++++")
        print(f"Running netperf with packets of size {i * 8} bits")
        rtt = run_netperf(ip, l_packets=i, sudo=s)
        overall_performances.append(rtt)

    return overall_performances, actual_hops
