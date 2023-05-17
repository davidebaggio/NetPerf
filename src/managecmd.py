import subprocess
from fileout import *
import pingparsing as pp
import socket

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
    if 'rtt_max' in stats:
        rtt.append(stats['rtt_max'])
    if 'rtt_min' in stats:
        rtt.append(stats['rtt_min'])
    if 'rtt_avg' in stats:
        rtt.append(stats['rtt_avg'])
    if 'rtt_mdev' in stats:
        rtt.append(stats['rtt_mdev'])
    return rtt

# get ttl


def get_ttl(ping_out: str):
    stats = parse_stats(ping_out)
    ttl = stats.icmp_replies[0]['ttl']
    return int(ttl)

# get times


def get_times(ping_out: str):
    stats = parse_stats(ping_out)
    times = []
    for icmp in stats.icmp_replies:
        if 'time' not in icmp:
            continue
        times.append(icmp['time'])
    return times


# run command


def run_command(command: list):
    cmd = " ".join(command)
    print("++++++++++++++++++++++++++++++++++++++++++++")
    print("Running command: " + cmd)
    return parse_output(subprocess.check_output(command))

# parse output


def parse_output(output):
    return output.decode('utf-8').strip()

# get lines of output


def get_lines(buffer: str):
    return buffer.split('\n')

# get ip


def get_ip(url):
    ip = socket.gethostbyname(url)
    return ip
