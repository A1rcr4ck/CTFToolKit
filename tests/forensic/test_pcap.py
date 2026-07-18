from scapy.all import Ether, IP, TCP, UDP, wrpcap
from scapy.layers.dns import DNS, DNSQR
from forensic.pcap import PcapAnalyzer
from scapy.layers.http import Raw


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