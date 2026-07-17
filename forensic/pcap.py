from collections import Counter
from scapy.all import rdpcap
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.http import HTTPRequest

class PcapAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.packets = rdpcap(filename)

    def summary(self):
        protocols = Counter()
        hosts = set()

        for pkt in self.packets:
            if IP in pkt:
                hosts.add(pkt[IP].src)
                hosts.add(pkt[IP].dst)

                proto = pkt[IP].proto

                if proto == 6:
                    protocols["TCP"] += 1
                elif proto == 17:
                    protocols["UDP"] += 1
                elif proto == 1:
                    protocols["ICMP"] += 1
                else:
                    protocols[f"PROTO-{proto}"] += 1

        return {
            "packets": len(self.packets),
            "hosts": sorted(hosts),
            "protocols": dict(protocols),
        }

    def hosts(self):
        counter = Counter()

        for pkt in self.packets:
            if IP in pkt:
                counter[pkt[IP].src] += 1
                counter[pkt[IP].dst] += 1

        return dict(counter)
    
    def conversations(self):
        counter = Counter()

        for pkt in self.packets:
            if IP not in pkt:
                continue

            src = pkt[IP].src
            dst = pkt[IP].dst

            if TCP in pkt:
                proto = "TCP"
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport

            elif UDP in pkt:
                proto = "UDP"
                sport = pkt[UDP].sport
                dport = pkt[UDP].dport

            else:
                proto = "IP"
                sport = "-"
                dport = "-"

            key = (src, dst, proto, sport, dport)
            counter[key] += 1

        return counter
    def dns_queries(self):
        queries = []

        for pkt in self.packets:
            if DNS in pkt and pkt[DNS].qr == 0:
                if DNSQR in pkt:
                    queries.append({
                        "name": pkt[DNSQR].qname.decode(errors="ignore").rstrip("."),
                        "type": pkt[DNSQR].qtype,
                    })

        return queries

    def http_requests(self):
        requests = []

        for pkt in self.packets:

            if HTTPRequest in pkt:

                http = pkt[HTTPRequest]

                requests.append({
                    "method": http.Method.decode(errors="ignore"),
                    "host": http.Host.decode(errors="ignore") if hasattr(http, "Host") else "",
                    "path": http.Path.decode(errors="ignore") if hasattr(http, "Path") else "",
                })

        return requests