import socket
import ipaddress
import concurrent.futures
import time

subnet = input("Enter the IP address subnet (in CIDR notation): ")
open_hosts = []

def check_port(ip):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect((str(ip), 2000))
            open_hosts.append(ip)
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3000) as executor:
        futures = [executor.submit(check_port, ip) for ip in ipaddress.IPv4Network(subnet)]
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                print(f"Port 2000 is open on {future.result()}")

start_time = time.time()
main()
elapsed_time = time.time() - start_time
num_requests = len(list(ipaddress.IPv4Network(subnet)))
requests_per_sec = num_requests / elapsed_time

print(f"Checked {num_requests} hosts in {elapsed_time:.2f} seconds")
print(f"Sent {requests_per_sec:.2f} requests per second")
print(f"Found {len(open_hosts)} hosts with port 2000 open")
