import socket
import platform
import os
import subprocess

def get_os_info():
    """
    Get basic operating system information.
    """
    os_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Platform": platform.platform(),
        "Processor": platform.processor()
    }
    return os_info

def get_ip_address():
    """
    Retrieve the server's IP address.
    """
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return {"Hostname": hostname, "IP Address": ip_address}

def scan_ports(target_ip, port_range=(1, 1024)):
    """
    Scan ports on the given IP to identify open and closed ports.
    """
    open_ports = []
    print(f"Scanning ports on {target_ip} in range {port_range}...")
    
    for port in range(port_range[0], port_range[1] + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
    
    return open_ports

def get_service_banner(target_ip, port):
    """
    Attempt to grab a service banner from an open port.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect((target_ip, port))
            banner = sock.recv(1024).decode().strip()
            return banner
    except Exception as e:
        return None

def list_open_ports_and_services(target_ip, ports):
    """
    List open ports along with any service banners detected.
    """
    open_ports_info = {}
    for port in ports:
        banner = get_service_banner(target_ip, port)
        open_ports_info[port] = banner if banner else "No banner detected"
    return open_ports_info

def display_server_profile(target_ip, port_range=(1, 1024)):
    """
    Display complete server profile including OS info, IP, open ports, and services.
    """
    print("\n--- Server Profile ---\n")
    
    # OS Information
    os_info = get_os_info()
    print("Operating System Information:")
    for key, value in os_info.items():
        print(f"  {key}: {value}")
    
    # IP Address
    ip_info = get_ip_address()
    print("\nNetwork Information:")
    for key, value in ip_info.items():
        print(f"  {key}: {value}")
    
    # Port Scan
    print("\nScanning for open ports...")
    open_ports = scan_ports(target_ip, port_range)
    
    if open_ports:
        print("\nOpen Ports Found:")
        open_ports_info = list_open_ports_and_services(target_ip, open_ports)
        for port, banner in open_ports_info.items():
            print(f"  Port {port}: {banner}")
    else:
        print("No open ports found.")
    
    print("\n--- End of Profile ---\n")

if __name__ == "__main__":
    # Input IP address to profile and port range (adjustable as needed)
    target_ip = input("Enter the target IP address: ")
    port_start = int(input("Enter the starting port: "))
    port_end = int(input("Enter the ending port: "))
    
    display_server_profile(target_ip, (port_start, port_end))
