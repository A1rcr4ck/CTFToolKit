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

            if TCP not in pkt:
                continue

            payload = bytes(pkt[TCP].payload)

            if not payload:
                continue

            try:
                text = payload.decode("utf-8", errors="ignore")
            except Exception:
                continue

            lines = text.split("\r\n")

            if not lines:
                continue

            first = lines[0]

            methods = (
                "GET",
                "POST",
                "PUT",
                "DELETE",
                "HEAD",
                "OPTIONS",
                "PATCH",
            )

            if not first.startswith(methods):
                continue

            parts = first.split()

            if len(parts) < 2:
                continue

            method = parts[0]
            path = parts[1]

            host = ""

            for line in lines:

                if line.lower().startswith("host:"):
                    host = line.split(":", 1)[1].strip()
                    break

            requests.append(
                {
                    "method": method,
                    "host": host,
                    "path": path,
                }
            )

        return requests
    
    def tls_info(self):
        results = []

        for pkt in self.packets:

            if TCP not in pkt:
                continue

            payload = bytes(pkt[TCP].payload)

            if len(payload) < 6:
                continue

            # TLS Record
            if payload[0] != 0x16:
                continue

            version_map = {
                b"\x03\x00": "SSL 3.0",
                b"\x03\x01": "TLS 1.0",
                b"\x03\x02": "TLS 1.1",
                b"\x03\x03": "TLS 1.2",
                b"\x03\x04": "TLS 1.3",
            }

            version = version_map.get(payload[1:3], "Unknown")

            handshake = payload[5]

            handshake_map = {
                1: "ClientHello",
                2: "ServerHello",
                11: "Certificate",
                12: "ServerKeyExchange",
                14: "ServerHelloDone",
                16: "ClientKeyExchange",
                20: "Finished",
            }

            results.append(
                {
                    "version": version,
                    "handshake": handshake_map.get(handshake, f"Type {handshake}"),
                }
            )

        return results
    
    def http_responses(self):
        responses = []

        for pkt in self.packets:

            if TCP not in pkt:
                continue

            payload = bytes(pkt[TCP].payload)

            if not payload:
                continue

            try:
                text = payload.decode("utf-8", errors="ignore")
            except Exception:
                continue

            lines = text.split("\r\n")

            if not lines:
                continue

            first = lines[0]

            if not first.startswith("HTTP/"):
                continue

            parts = first.split()

            if len(parts) < 3:
                continue

            status = parts[1]
            reason = " ".join(parts[2:])

            server = ""
            content_type = ""

            for line in lines:
                lower = line.lower()

                if lower.startswith("server:"):
                    server = line.split(":", 1)[1].strip()

                elif lower.startswith("content-type:"):
                    content_type = line.split(":", 1)[1].strip()

            responses.append({
                "status": status,
                "reason": reason,
                "server": server,
                "content_type": content_type,
            })

        return responses