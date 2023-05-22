import subprocess
from fileout import *
import socket

# run command

def run_command(command: list):
    cmd = " ".join(command)
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
