import platform

os_name = platform.system()

def get_linux_distro():
    with open('/etc/os-release', 'r') as f:
        for line in f:
            if line.startswith('ID='):
                distro_id = line.split('=')[1].strip().strip('"')
                distro = distro_id
    return distro

def determine_os():
    if os_name == "Windows":
        return "windows"
    elif os_name == "Linux":
        return get_linux_distro()
    elif os_name == "Darwin":
        return "mac"
    else:
        print("Unsupported operating system")