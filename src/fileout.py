
# output to file


def output_to_file(ip: str, ping: str):
    output_file = define_output_file(ip)
    f = open(output_file, 'w')
    f.write(ping)
    f.close()

# define output file based on ip address


def define_output_file(ip_address: str):
    return "output/" + ip_address.replace(".", "_") + ".txt"
