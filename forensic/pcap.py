import os
from pathlib import Path
from collections import Counter
from scapy.all import rdpcap
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.http import HTTPRequest
import base64

from core import output

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
    
    def credentials(self):
        credentials = []

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

            for line in text.split("\r\n"):

                lower = line.lower()

                if lower.startswith("authorization: basic "):

                    encoded = line.split(" ", 2)[2].strip()

                    try:
                        decoded = base64.b64decode(encoded).decode(
                            "utf-8",
                            errors="ignore",
                        )
                    except Exception:
                        decoded = "<invalid>"

                    credentials.append(
                        {
                            "type": "Basic Auth",
                            "value": decoded,
                        }
                    )

                elif lower.startswith("authorization: bearer "):

                    token = line.split(" ", 2)[2].strip()

                    credentials.append(
                        {
                            "type": "Bearer Token",
                            "value": token,
                        }
                    )

                elif lower.startswith("cookie:"):

                    cookie = line.split(":", 1)[1].strip()

                    credentials.append(
                        {
                            "type": "Cookie",
                            "value": cookie,
                        }
                    )

        return credentials
    
    def carve_files(self, output_dir):
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        signatures = [
            (
                b"\x89PNG\r\n\x1a\n",
                b"IEND\xaeB`\x82",
                ".png",
            ),
            (
                b"%PDF",
                b"%%EOF",
                ".pdf",
            ),
            (
                b"PK\x03\x04",
                None,
                ".zip",
            ),
            (
                b"\xff\xd8",
                b"\xff\xd9",
                ".jpg",
            ),
        ]

        recovered = []
        counter = 1

        for pkt in self.packets:

            if TCP not in pkt:
                continue

            payload = bytes(pkt[TCP].payload)

            if not payload:
                continue

            for start_sig, end_sig, ext in signatures:

                start = payload.find(start_sig)

                if start == -1:
                    continue

                if end_sig:

                #     end = payload.find(end_sig, start)

                #     if end == -1:
                #         continue

                #     end += len(end_sig)
                #     data = payload[start:end]

                # else:
                    data = payload[start:]

                filename = output / f"{counter:04d}{ext}"

                with open(filename, "wb") as f:
                    f.write(data)

                recovered.append(str(filename))

                counter += 1

        return recovered
    
    def tcp_streams(self):
        streams = {}

        for pkt in self.packets:

            if IP not in pkt or TCP not in pkt:
                continue

            key = (
                pkt[IP].src,
                pkt[TCP].sport,
                pkt[IP].dst,
                pkt[TCP].dport,
            )

            payload = bytes(pkt[TCP].payload)

            if not payload:
                continue

            streams.setdefault(key, []).append(
                (
                    pkt[TCP].seq,
                    payload,
                )
            )

        result = []

        for key, packets in streams.items():

            packets.sort(key=lambda x: x[0])

            data = b"".join(
                payload
                for _, payload in packets
            )

            result.append(
                {
                    "src": key[0],
                    "sport": key[1],
                    "dst": key[2],
                    "dport": key[3],
                    "size": len(data),
                    "data": data,
                }
            )

        return result
    
    def export_streams(self, output_dir):
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        exported = []

        for index, stream in enumerate(self.tcp_streams(), start=1):

            filename = (
                output
                / (
                    f"{index:04d}_"
                    f"{stream['src']}_"
                    f"{stream['sport']}_"
                    f"{stream['dst']}_"
                    f"{stream['dport']}.bin"
                )
            )

            with open(filename, "wb") as f:
                f.write(stream["data"])

            exported.append(str(filename))

        return exported
    
    # def _decode_chunked(self, body):

    #     decoded = b""
    #     offset = 0

    #     while True:

    #         end = body.find(b"\r\n", offset)

    #         if end == -1:
    #             break

    #         try:
    #             size = int(body[offset:end].decode(), 16)
    #         except ValueError:
    #             break

    #         offset = end + 2

    #         if size == 0:
    #             break

    #         decoded += body[offset:offset + size]

    #         offset += size + 2

    #     return decoded
    
    def http_bodies(self):
        bodies = []

        for stream in self.tcp_streams():

            data = stream["data"]

            if b"\r\n\r\n" not in data:
                continue

            header, remaining = data.split(b"\r\n\r\n", 1)

            try:
                header_text = header.decode(errors="replace")
            except Exception:
                continue

            lines = header_text.splitlines()

            if not lines:
                continue

            first = lines[0]

            if not (
                first.startswith("GET")
                or first.startswith("POST")
                or first.startswith("PUT")
                or first.startswith("HTTP/")
            ):
                continue

            headers = {}

            for line in lines[1:]:

                if ":" not in line:
                    continue

                key, value = line.split(":", 1)

                headers[key.strip().lower()] = value.strip()

                filename = None

                content_disposition = headers.get("content-disposition", "")

                if "filename=" in content_disposition:

                    filename = content_disposition.split("filename=", 1)[1].strip()

                    if filename.startswith('"') and filename.endswith('"'):
                        filename = filename[1:-1]

                    filename = os.path.basename(filename)

            if headers.get("content-length"):

                try:
                    expected = int(headers["content-length"])
                    body = remaining[:expected]
                except ValueError:
                    body = remaining

            else:
                body = remaining

            bodies.append(
                {
                    "src": stream["src"],
                    "dst": stream["dst"],
                    "host": headers.get("host"),
                    "content_type": headers.get("content-type"),
                    "filename": filename,
                    "content_length": len(body),
                    "expected_length": (
                        int(headers["content-length"])
                        if headers.get("content-length", "").isdigit()
                        else None
                    ),
                    "body": body,
                }
            )

        return bodies
    
    def extract_http_objects(self, output_dir):
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        extracted = []

        for index, body in enumerate(self.http_bodies(), start=1):

            filename = body.get("filename")

            if filename:

                filename = output / filename

            else:

                content_type = body.get("content_type") or ""

                extension = ".bin"

                if "text/plain" in content_type:
                    extension = ".txt"
                elif "text/html" in content_type:
                    extension = ".html"
                elif "application/pdf" in content_type:
                    extension = ".pdf"
                elif "application/zip" in content_type:
                    extension = ".zip"
                elif "image/png" in content_type:
                    extension = ".png"
                elif "image/jpeg" in content_type:
                    extension = ".jpg"

                filename = output / f"http_object_{index:04d}{extension}"

            with open(filename, "wb") as f:
                f.write(body["body"])

            extracted.append(str(filename))

        return extracted