import socket
import argparse
import concurrent.futures
import logging
import time
from datetime import datetime

# logs config
logging.basicConfig(level=logging.INFO, format='%(message)s')


class Pymap:

    def __init__(self, target, start_port, end_port,timeout=0.8):
        self.target = target
        self.ports = range(start_port, end_port + 1)
        self.timeout = timeout
        self.results = []

    def get_service_name(self,port):
        try:
            return socket.getservbyport(port,"tcp").upper()
        except OSError:
            return "UNKNOWN"

    def grab_banner(self, sock, port):
        try:
            if port in(80,1000,443):
                sock.send(b"HEAD / HTTP/1.1\r\nHOST:"+ self.target.encode() + b"\r\n\r\n")
            else:
                sock.send(b"\r\n")

            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()

            return banner.split('\r\n')[0][:35] if banner else "Sem banner"

        except Exception:
            return "Sem banner"

    def scan_port(self,port):
        """try to connect on port"""
        try:
            #AF_INET=Ipv4,SOCK_STREAM=TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)   #short timeout for quick scan
                start_time = time.time()
                result = s.connect_ex((self.target, port))
                latency = (time.time() - start_time) * 1000

                if result == 0:
                    service = self.get_service_name(port)
                    banner = self.grab_banner(s, port)
                    return {
                        "port": f"{port}/tcp",
                        "service": service,
                        "latency": f"{latency:.1f} ms",
                        "banner": banner
                    }
        except socket.timeout:
            return "Timeout"
        except OSError:
            return "Socket Error"

        return None

    def run(self, threads=50):
        logging.info(f"Starting Nmap Scan on {self.target} at {datetime.now()}")
        logging.info("-" * 50)

        start_scan = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.scan_port, port) for port in self.ports]
            for futures in concurrent.futures.as_completed(futures):
                res = futures.result()
                if res:
                    self.results.append(res)
        self.results.sort(key=lambda x: int(x["port"].split('/')[0]))
        total_time = time.time() - start_scan
        self._display_table(total_time)

    def _display_table(self,elapsed_time):

        header_format = "{:<12} {:<12} {:12} {:<35}"
        print("="*75)
        print(header_format.format("Port", "service", "latency","banner"))
        print("="*75)

        if not self.results:
            print("No ports open found")
        else:
            for item in self.results:
                print(header_format.format(
                    item["port"],
                    item["service"],
                    item["latency"],
                    item["banner"]
                ))
            print("="*75)
            print(f"[+] Scan Complete on {elapsed_time:.2f}s.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="PyMap - Fast TCP port scan")
    parser.add_argument("host", help="ip or target domain (ex: scame.nmap.org)")
    parser.add_argument("-p", "--ports", help="Ports interval (ex:1-1024", default="1-1024")
    parser.add_argument("-t", "--threads", help="Threads on use",type=int,default=50)

    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.host)
        start_p,end_p = map(int, args.ports.split('-'))
        scanner = Pymap(target_ip, start_p, end_p)
        scanner.run()
    except socket.gaierror:
        logging.error("Error: invalid Host or host is down")
    except ValueError:
        logging.error("Error:invalid Format")
