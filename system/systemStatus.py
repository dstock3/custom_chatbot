import psutil

def get_system_data():
    mem = psutil.virtual_memory()
    cpu_usage = psutil.cpu_percent()
    avg_load = psutil.getloadavg()
    temp = psutil.sensors_temperatures()

    return {'mem': mem, 'cpu_usage': cpu_usage, 'avg_load': avg_load, 'temp': temp}

def get_network_data():
    network_data = psutil.net_io_counters()
    return network_data
