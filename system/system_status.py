import psutil

def bytes_to_human(n):
    symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
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

def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    total_disk = bytes_to_human(disk_usage.total)
    used_disk = bytes_to_human(disk_usage.used)
    free_disk = bytes_to_human(disk_usage.free)
    used_disk_percentage = disk_usage.percent

    return {
        'total': total_disk,
        'used': used_disk,
        'free': free_disk,
        'used_percent': used_disk_percentage
    }

def get_running_processes(sort_by):
    all_processes = []

    for process in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        all_processes.append(process.info)

    if sort_by == 'memory':
        top_processes = sorted(all_processes, key=lambda x: x['memory_percent'], reverse=True)[:10]
    elif sort_by == 'cpu':
        top_processes = sorted(all_processes, key=lambda x: x['cpu_percent'], reverse=True)[:10]
    else:
        raise ValueError("sort_by should be either 'memory' or 'cpu'")

    return top_processes

def get_memory_intensive_processes():
    return get_running_processes('memory')

def get_cpu_intensive_processes():
    return get_running_processes('cpu')
