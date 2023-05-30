from linux import main as linuxmain
from windows import main as windowsmain
import managecmd
import calculation
import os


# detect operating system
def detect_os():
    if os.name == "nt":
        return "windows"
    elif os.name == "posix":
        return "linux"
    else:
        return "unknown"


# running network performance
if __name__ == "__main__":
    host = input("Insert hostname, skip by pressing enter. The default hostname is \'lon.speedtest.clouvider.net\' \n--> ")
    if host.strip() == "":
        host = "lon.speedtest.clouvider.net"
    ip = managecmd.get_ip(host)
    print(f"IP: {ip}")
    steps = list(range(64, 1472, 16))
    
    os = detect_os()
    if os == "windows":
        overall_performances, actual_hops = windowsmain(ip, steps)
    elif os == "linux":
        overall_performances, actual_hops = linuxmain(ip, steps)
    else:
        print("Unknown operating system")
        exit(1)
    
    # change steps from byte to all bit
    for i in range(len(steps)):
        steps[i] = (steps[i] + 28) * 8
    
    calculation.plot_all(steps, overall_performances)
    s, s_b, t = calculation.calculate_throughput(steps, overall_performances, actual_hops)
    
    print(f"Throughput: {s} bits/s")
    print(f"Throughput Bottleneck: {s_b} bits/s")
    print(f"Time of propagation: {t} ms")
