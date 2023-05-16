
# output to file
def output_to_file(ip: str, ping: str, trace: str, ttl: int):
    output_file = define_output_file(ip)
    f = open(output_file, 'w')
    f.write("\n------------- Ping -------------\n")
    f.write(ping)
    f.write("\n\n------------- Trace -------------\n")
    f.write(trace)
    f.write("\n\n------------- TTL -------------\n")
    f.write(str(64 - ttl + 1))
    f.write("\n")
    f.close()

# define output file based on ip address


def define_output_file(ip_address: str):
    return "output/" + ip_address.replace(".", "_") + ".txt"
