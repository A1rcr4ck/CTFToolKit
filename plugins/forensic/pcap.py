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

    parser.add_argument(
        "--credentials",
        action="store_true",
        help="Extract credentials from HTTP traffic",
    )

    parser.add_argument(
        "--carve",
        metavar="DIR",
        help="Recover embedded files into a directory",
    )

    parser.add_argument(
        "--streams",
        action="store_true",
        help="Reassemble TCP streams",
    )

    parser.add_argument(
        "--export-streams",
        metavar="DIR",
        help="Export reconstructed TCP streams",
    )

    parser.add_argument(
        "--http-body",
        action="store_true",
        help="Extract HTTP bodies from TCP streams",
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

    if args.credentials:

        result = analyzer.credentials()

        if args.output == OutputFormat.JSON.value:
            dispatch(
                OutputFormat.JSON.value,
                json_data=result,
            )
            return

        rows = []

        for item in result:
            rows.append(
                [
                    item["type"],
                    item["value"],
                ]
            )

        dispatch(
            OutputFormat.TABLE.value,
            table_data=(
                "Credentials",
                ["Type", "Value"],
                rows,
            ),
        )

        return
    
    if args.carve:

        result = analyzer.carve_files(args.carve)

        if args.output == OutputFormat.JSON.value:
            dispatch(
                OutputFormat.JSON.value,
                json_data=result,
            )
            return

        rows = []

        for file in result:
            rows.append([file])

        dispatch(
            OutputFormat.TABLE.value,
            table_data=(
                "Recovered Files",
                ["Filename"],
                rows,
            ),
        )

        return
    
    if args.streams:

        result = analyzer.tcp_streams()

        if args.output == OutputFormat.JSON.value:
            dispatch(
                OutputFormat.JSON.value,
                json_data=[
                    {
                        **stream,
                        "data": stream["data"].decode(
                            "utf-8",
                            errors="replace",
                        ),
                    }
                    for stream in result
                ],
            )
            return

        rows = []

        for stream in result:

            rows.append(
                [
                    stream["src"],
                    stream["sport"],
                    stream["dst"],
                    stream["dport"],
                    stream["size"],
                ]
            )

        dispatch(
            OutputFormat.TABLE.value,
            table_data=(
                "TCP Streams",
                [
                    "Source",
                    "Src Port",
                    "Destination",
                    "Dst Port",
                    "Bytes",
                ],
                rows,
            ),
        )

        return
    
    if args.export_streams:

        result = analyzer.export_streams(args.export_streams)

        if args.output == OutputFormat.JSON.value:
            dispatch(
                OutputFormat.JSON.value,
                json_data=result,
            )
            return

        rows = []

        for file in result:
            rows.append([file])

        dispatch(
            OutputFormat.TABLE.value,
            table_data=(
                "Exported Streams",
                ["Filename"],
                rows,
            ),
        )

        return
    
    if args.http_body:

        result = analyzer.http_bodies()

        if args.output == OutputFormat.JSON.value:

            dispatch(
                OutputFormat.JSON.value,
                json_data=[
                    {
                        **body,
                        "body": body["body"].decode(
                            "utf-8",
                            errors="replace",
                        ),
                    }
                    for body in result
                ],
            )
            return

        rows = []

        for body in result:

            rows.append(
                [
                    body["host"],
                    body["content_type"],
                    body["content_length"],
                ]
            )

        dispatch(
            OutputFormat.TABLE.value,
            table_data=(
                "HTTP Bodies",
                [
                    "Host",
                    "Content-Type",
                    "Bytes",
                ],
                rows,
            ),
        )

        return
    