from managecmd import *
from fileout import *


# get rtt


def get_rtt(ping_out: str):
    rtt = get_lines(ping_out)[-1].split()[-2].split('/')
    return list(map(float, rtt))

# get ttl


def get_ttl(ping_out: str):
    return int(get_lines(ping_out)[1].split()[-3].split('=')[-1])


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

    if info:
        trace = traceroute(ip, sudo=sudo)
        ttl = get_ttl(out)
        length = len(get_lines(trace)) - 1
        print(length)
        if (64 - ttl + 1) == length:
            print("TTL is correct")

        print(out)
        print(trace)
        print("RTT: ")
        print(rtt)
        output_to_file(ip, out, trace, ttl)

    return rtt


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

    ip = "atl.speedtest.clouvider.net"

    run_netperf(ip, l_packets=10, sudo=s, info=True)

    overall_performances = []
    steps = list(range(64, 1472, 64))

    for i in steps:
        print("-----------------------")
        print(f"Running netperf with packets of size {i * 8} bits")
        overall_performances.append(run_netperf(ip, l_packets=i, sudo=s))
