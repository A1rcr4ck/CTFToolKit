from pathlib import Path

from scapy.all import Ether, IP, TCP, UDP, wrpcap
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.http import Raw

from forensic.pcap import PcapAnalyzer


def test_hosts(tmp_path):
    pcap = tmp_path / "sample.pcap"

    packets = [
        Ether()/IP(src="10.0.0.1", dst="10.0.0.2")/TCP(),
        Ether()/IP(src="10.0.0.1", dst="10.0.0.3")/TCP(),
    ]

    wrpcap(str(pcap), packets)

    result = PcapAnalyzer(str(pcap)).hosts()

    assert result["10.0.0.1"] == 2
    assert result["10.0.0.2"] == 1
    assert result["10.0.0.3"] == 1

def test_conversations(tmp_path):
    pcap = tmp_path / "sample.pcap"

    packets = [
        Ether()/IP(src="10.0.0.1", dst="10.0.0.2")/TCP(sport=1111, dport=80),
        Ether()/IP(src="10.0.0.1", dst="10.0.0.2")/TCP(sport=1111, dport=80),
        Ether()/IP(src="10.0.0.2", dst="10.0.0.1")/UDP(sport=53, dport=4444),
    ]

    wrpcap(str(pcap), packets)

    result = PcapAnalyzer(str(pcap)).conversations()

    assert result[("10.0.0.1", "10.0.0.2", "TCP", 1111, 80)] == 2
    assert result[("10.0.0.2", "10.0.0.1", "UDP", 53, 4444)] == 1

def test_dns_queries(tmp_path):
    pcap = tmp_path / "dns.pcap"

    packets = [
        Ether()
        / IP(src="10.0.0.1", dst="8.8.8.8")
        / UDP(sport=12345, dport=53)
        / DNS(rd=1, qd=DNSQR(qname="openai.com"))
    ]

    wrpcap(str(pcap), packets)

    result = PcapAnalyzer(str(pcap)).dns_queries()

    assert len(result) == 1
    assert result[0]["name"] == "openai.com"

def test_http_requests(tmp_path):
    pcap = tmp_path / "http.pcap"

    pkt = (
        IP(src="10.0.0.1", dst="10.0.0.2")
        / TCP(sport=12345, dport=80)
        / Raw(
            load=(
                b"GET /index.html HTTP/1.1\r\n"
                b"Host: example.com\r\n"
                b"User-Agent: Test\r\n\r\n"
            )
        )
    )

    wrpcap(str(pcap), [pkt])

    result = PcapAnalyzer(str(pcap)).http_requests()

    assert len(result) == 1
    assert result[0]["method"] == "GET"
    assert result[0]["host"] == "example.com"
    assert result[0]["path"] == "/index.html"

def test_tls_info(tmp_path):

    pcap = tmp_path / "tls.pcap"

    payload = (
        b"\x16"
        b"\x03\x03"
        b"\x00\x31"
        b"\x01"
        + b"\x00" * 48
    )

    pkt = (
        IP(src="10.0.0.1", dst="10.0.0.2")
        / TCP(sport=55555, dport=443)
        / Raw(load=payload)
    )

    wrpcap(str(pcap), [pkt])

    result = PcapAnalyzer(str(pcap)).tls_info()

    assert len(result) == 1
    assert result[0]["version"] == "TLS 1.2"
    assert result[0]["handshake"] == "ClientHello"

def test_http_responses(tmp_path):

    pcap = tmp_path / "response.pcap"

    pkt = (
        IP(src="10.0.0.2", dst="10.0.0.1")
        / TCP(sport=80, dport=12345)
        / Raw(
            load=(
                b"HTTP/1.1 200 OK\r\n"
                b"Server: nginx\r\n"
                b"Content-Type: text/html\r\n\r\n"
            )
        )
    )

    wrpcap(str(pcap), [pkt])

    result = PcapAnalyzer(str(pcap)).http_responses()

    assert result[0]["status"] == "200"
    assert result[0]["reason"] == "OK"
    assert result[0]["server"] == "nginx"
    assert result[0]["content_type"] == "text/html"

def test_credentials(tmp_path):

    pcap = tmp_path / "cred.pcap"

    pkt = (
        IP(src="10.0.0.1", dst="10.0.0.2")
        / TCP(sport=12345, dport=80)
        / Raw(
            load=(
                b"GET / HTTP/1.1\r\n"
                b"Host: example.com\r\n"
                b"Authorization: Basic YWRtaW46cGFzc3dvcmQ=\r\n"
                b"Cookie: PHPSESSID=abc123\r\n\r\n"
            )
        )
    )

    wrpcap(str(pcap), [pkt])

    result = PcapAnalyzer(str(pcap)).credentials()

    assert len(result) == 2
    assert result[0]["type"] == "Basic Auth"
    assert result[0]["value"] == "admin:password"
    assert result[1]["type"] == "Cookie"

def test_file_carving(tmp_path):

    pcap = tmp_path / "carve.pcap"

    png = (
        b"\x89PNG\r\n\x1a\n"
        + b"TESTDATA"
        + b"IEND\xaeB`\x82"
    )

    pkt = (
        IP(src="1.1.1.1", dst="2.2.2.2")
        / TCP()
        / Raw(load=png)
    )

    wrpcap(str(pcap), [pkt])

    outdir = tmp_path / "output"

    recovered = PcapAnalyzer(str(pcap)).carve_files(outdir)

    assert len(recovered) == 1
    assert Path(recovered[0]).exists()
    assert recovered[0].endswith(".png")

def test_tcp_streams(tmp_path):

    pcap = tmp_path / "streams.pcap"

    pkt1 = (
        IP(src="10.0.0.1", dst="10.0.0.2")
        / TCP(sport=1234, dport=80, seq=1)
        / Raw(load=b"Hello ")
    )

    pkt2 = (
        IP(src="10.0.0.1", dst="10.0.0.2")
        / TCP(sport=1234, dport=80, seq=7)
        / Raw(load=b"World")
    )

    wrpcap(str(pcap), [pkt1, pkt2])

    result = PcapAnalyzer(str(pcap)).tcp_streams()

    assert len(result) == 1
    assert result[0]["data"] == b"Hello World"
    assert result[0]["size"] == 11

def test_export_streams(tmp_path):

    pcap = tmp_path / "streams.pcap"

    pkt1 = (
        IP(src="10.0.0.1", dst="10.0.0.2")
        / TCP(sport=1234, dport=80, seq=1)
        / Raw(load=b"Hello ")
    )

    pkt2 = (
        IP(src="10.0.0.1", dst="10.0.0.2")
        / TCP(sport=1234, dport=80, seq=7)
        / Raw(load=b"World")
    )

    wrpcap(str(pcap), [pkt1, pkt2])

    outdir = tmp_path / "streams"

    exported = PcapAnalyzer(str(pcap)).export_streams(outdir)

    assert len(exported) == 1

    exported_file = Path(exported[0])

    assert exported_file.exists()
    assert exported_file.read_bytes() == b"Hello World"