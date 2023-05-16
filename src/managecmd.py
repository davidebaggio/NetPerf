import subprocess

# ping command
def ping(ip, n=1, ttl=64, size=64, sudo=False):
    if sudo:
        return run_command(['sudo', 'ping', '-c', str(n), '-t', str(ttl), '-s', str(size), ip])
    else:
        return run_command(['ping', '-c', str(n), '-t', str(ttl), '-s', str(size), ip])

# traceroute command
def traceroute(ip, sudo=False):
    if sudo:
        return run_command(['sudo', 'traceroute', ip])
    else:
        return run_command(['traceroute', ip])

# run command
def run_command(command: list):
    cmd = " ".join(command)
    print("Running command: " + cmd)
    return parse_output(subprocess.check_output(command))

# parse output
def parse_output(output):
    return output.decode('utf-8').strip()

# get lines of output
def get_lines(ping_out: str):
    return ping_out.split('\n')

# get ttl
def get_ttl(ping_out: str):
    return int(get_lines(ping_out)[1].split()[-3].split('=')[-1])

# get rtt
def get_rtt(ping_out: str):
    return get_lines(ping_out)[-1].split()[-2].split('/')