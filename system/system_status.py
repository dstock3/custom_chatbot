import psutil

def bytes_to_human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f %s' % (value, s)
    return "%s B" % n

def get_system_data():
    mem = psutil.virtual_memory()
    cpu_usage = psutil.cpu_percent()
    avg_load = psutil.getloadavg()
    temp = psutil.sensors_temperatures()

    total_mem = bytes_to_human(mem.total)
    available_mem = bytes_to_human(mem.available)
    used_mem_percentage = mem.percent

    return {
        'mem': {
            'total': total_mem, 
            'available': available_mem, 
            'used_percent': used_mem_percentage
        },
        'cpu_usage': cpu_usage,
        'avg_load': avg_load,
        'temp': temp
    }

def get_network_data():
    network_data = psutil.net_io_counters()
    bytes_sent = bytes_to_human(network_data.bytes_sent)
    bytes_recv = bytes_to_human(network_data.bytes_recv)
    packets_sent = network_data.packets_sent
    packets_recv = network_data.packets_recv

    return {
        'bytes_sent': bytes_sent,
        'bytes_recv': bytes_recv,
        'packets_sent': packets_sent,
        'packets_recv': packets_recv
    }
