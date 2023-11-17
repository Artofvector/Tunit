import socket

def get_ip_address(domain):
    if "https://" in domain:
        domain = domain.split('https://')[1]
    elif "http://" in domain:
        domain = domain.split('http://')[1]
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None
