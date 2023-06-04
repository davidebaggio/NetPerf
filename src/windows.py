from managecmd import *
from fileout import *
import re
import statistics
import calculation

# print info


def route_info(ip: str):
    print("-------------Finding amount of hops to the host-------------")
    count_hops = 30
    while count_hops > 0:
        try:
            ping(ip, n=1, ttl=count_hops, size=1)
            count_hops -= 1
        except Exception:
            count_hops += 1
            break
    print("------------------------------------------------------------")
    if count_hops == 0:
        print("No links found, connection might be timed out")
        exit(1)

    ping_info = ping(ip, n=10, ttl=64, size=64)
    print(ping_info)
    print("------------------------------------")

    trace = tracert(ip)
    print(trace)
    print("------------------------------------")

    length = len(get_lines(trace)) - 4
    if length == 30:
        print("Max hops reached, Connection might be timed out")
        exit(1)

    if count_hops == length:
        print("Route is correct")
    print(f"Hops to host: {count_hops}")
    output_to_file(ip, ping_info)

    return count_hops


# get rtt


def get_rtt(ping_out: str):
    rttLine = get_lines(ping_out)[-1].split(',')
    rtt = []
    for l in rttLine:
        rtt.append(l.split('=')[1].split()[-1][:-2])
    rtt[1], rtt[2] = rtt[2], rtt[1]
    return list(map(float, rtt))


# tracert command
def tracert(ip):
    return run_command(['tracert', '-d', ip])


# ping command
def ping(ip, n, ttl, size):
    return run_command(['ping', '-n', str(n), '-i', str(ttl), '-l', str(size), ip])


# psping command
def psping(ip, n, size):
    return run_command(['psping', '-n', str(n), '-i', '0', '-l', str(size), ip])


# get stdev
def get_stdev(out: str):
    round_trip_times = re.findall(r": (\d+\.\d+)ms", out)
    round_trip_times = list(map(float, round_trip_times))
    # print(out)
    # print(round_trip_times)
    stdev = statistics.pstdev(round_trip_times)
    return stdev


# net performance
def run_netperf(ip: str, k_packets=20, l_packets=64):

    ping_info = psping(ip, n=k_packets, size=l_packets)
    rtt = get_rtt(ping_info)
    rtt.append(get_stdev(ping_info))

    return rtt


def main(ip: str, steps: list):

    hops = route_info(ip)
    actual_hops = hops * 2
    print(f"Number of links crossed: {actual_hops}")

    overall_performances = []

    for i in steps:
        print("++++++++++++++++++++++++++++++++++++++++++++")
        print(f"Running netperf with packets of size {i * 8} bits")
        rtt = run_netperf(ip, l_packets=i)
        overall_performances.append(rtt)

    return overall_performances, actual_hops
