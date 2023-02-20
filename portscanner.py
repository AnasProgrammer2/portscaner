import socket
import ipaddress
import concurrent.futures
import time

subnet = input("Enter the IP address subnet (in CIDR notation): ")

def check_port(ip, ports):
    open_port_count = 0
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                sock.connect((str(ip), port))
                open_port_count += 1
                print(f"Port {port} is open on {ip}")
        except (socket.timeout, ConnectionRefusedError):
            pass
    return open_port_count

def main():
    ports = [80, 443]
    open_port_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=2000) as executor:
        results = {executor.submit(check_port, ip, ports): ip for ip in ipaddress.IPv4Network(subnet)}
        for future in concurrent.futures.as_completed(results):
            ip = results[future]
            try:
                open_port_count += future.result()
            except:
                pass

    print(f"Found {open_port_count} hosts with open port 2000")
    num_requests = len(list(ipaddress.IPv4Network(subnet)))
    elapsed_time = time.time() - start_time
    requests_per_sec = num_requests / elapsed_time
    print(f"Checked {num_requests} hosts in {elapsed_time:.2f} seconds")
    print(f"Sent {requests_per_sec:.2f} requests per second")

start_time = time.time()
main()
