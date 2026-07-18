from forensic.pcap import PcapAnalyzer
from core.output.dispatcher import dispatch
from core.output.formatter import OutputFormat


def register_pcap(subparsers):
    parser = subparsers.add_parser(
        "pcap",
        help="Analyze a PCAP capture",
    )

    parser.add_argument("file")

    parser.add_argument(
        "--hosts",
        action="store_true",
        help="Show hosts",
    )

    parser.add_argument(
        "--conversations",
        action="store_true",
        help="Show conversations",
    )

    parser.add_argument(
        "--dns",
        action="store_true",
        help="Show DNS queries",
    )

    parser.add_argument(
        "--http",
        action="store_true",
        help="Show HTTP requests",
    )

    parser.add_argument(
        "--http-response",
        action="store_true",
        help="Show HTTP responses",
    )

    parser.add_argument(
        "--tls",
        action="store_true",
        help="Show TLS handshake information",
    )

    parser.add_argument(
        "--output",
        choices=[
            OutputFormat.TABLE.value,
            OutputFormat.JSON.value,
        ],
        default=OutputFormat.TABLE.value,
    )

    parser.set_defaults(func=pcap_command)


def pcap_command(args):
    analyzer = PcapAnalyzer(args.file)

    # ---------------- Hosts ----------------

    if args.hosts:

        result = analyzer.hosts()

        if args.output == OutputFormat.JSON.value:
            dispatch(
                OutputFormat.JSON.value,
                json_data=result,
            )
            return

        rows = []

        for host, count in sorted(result.items()):
            rows.append([host, count])

        dispatch(
            OutputFormat.TABLE.value,
            table_data=(
                "Hosts",
                ["Host", "Packets"],
                rows,
            ),
        )
        return

    # ---------------- Conversations ----------------

    if args.conversations:

        result = analyzer.conversations()

        if args.output == OutputFormat.JSON.value:
            dispatch(
                OutputFormat.JSON.value,
                json_data={
                    f"{src}->{dst}:{proto}:{sport}->{dport}": count
                    for (src, dst, proto, sport, dport), count in result.items()
                },
            )
            return

        rows = []

        for (src, dst, proto, sport, dport), count in result.items():
            rows.append([
                src,
                dst,
                proto,
                sport,
                dport,
                count,
            ])

        dispatch(
            OutputFormat.TABLE.value,
            table_data=(
                "Conversations",
                [
                    "Source",
                    "Destination",
                    "Proto",
                    "Src Port",
                    "Dst Port",
                    "Packets",
                ],
                rows,
            ),
        )
        return

    # ---------------- DNS ----------------

    if args.dns:

        result = analyzer.dns_queries()

        if args.output == OutputFormat.JSON.value:
            dispatch(
                OutputFormat.JSON.value,
                json_data=result,
            )
            return

        rows = []

        for query in result:
            rows.append([
                query["name"],
                query["type"],
            ])

        dispatch(
            OutputFormat.TABLE.value,
            table_data=(
                "DNS Queries",
                ["Domain", "Type"],
                rows,
            ),
        )
        return

    # ---------------- HTTP Requests ----------------

    if args.http:

        result = analyzer.http_requests()

        if args.output == OutputFormat.JSON.value:
            dispatch(
                OutputFormat.JSON.value,
                json_data=result,
            )
            return

        rows = []

        for req in result:
            rows.append([
                req["method"],
                req["host"],
                req["path"],
            ])

        dispatch(
            OutputFormat.TABLE.value,
            table_data=(
                "HTTP Requests",
                ["Method", "Host", "Path"],
                rows,
            ),
        )
        return

    # ---------------- HTTP Responses ----------------

    if args.http_response:

        result = analyzer.http_responses()

        if args.output == OutputFormat.JSON.value:
            dispatch(
                OutputFormat.JSON.value,
                json_data=result,
            )
            return

        rows = []

        for item in result:
            rows.append([
                item["status"],
                item["reason"],
                item["server"],
                item["content_type"],
            ])

        dispatch(
            OutputFormat.TABLE.value,
            table_data=(
                "HTTP Responses",
                ["Status", "Reason", "Server", "Content-Type"],
                rows,
            ),
        )
        return

    # ---------------- TLS ----------------

    if args.tls:

        result = analyzer.tls_info()

        if args.output == OutputFormat.JSON.value:
            dispatch(
                OutputFormat.JSON.value,
                json_data=result,
            )
            return

        rows = []

        for item in result:
            rows.append([
                item["version"],
                item["handshake"],
            ])

        dispatch(
            OutputFormat.TABLE.value,
            table_data=(
                "TLS Information",
                ["Version", "Handshake"],
                rows,
            ),
        )
        return

    # ---------------- Summary ----------------

    result = analyzer.summary()

    if args.output == OutputFormat.JSON.value:
        dispatch(
            OutputFormat.JSON.value,
            json_data=result,
        )
        return

    rows = [
        ["Packets", result["packets"]],
        ["Unique Hosts", len(result["hosts"])],
        ["Protocols", ", ".join(result["protocols"].keys())],
    ]

    dispatch(
        OutputFormat.TABLE.value,
        table_data=(
            "PCAP Summary",
            ["Field", "Value"],
            rows,
        ),
    )