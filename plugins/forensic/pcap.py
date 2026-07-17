from forensic.pcap import PcapAnalyzer
from core.output.dispatcher import dispatch
from core.output.formatter import OutputFormat


def register_pcap(subparsers):
    parser = subparsers.add_parser(
        "pcap",
        help="Analyze a PCAP capture"
    )

    parser.add_argument("file")

    parser.add_argument(
        "--hosts",
        action="store_true",
        help="Show hosts"
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

    parser.set_defaults(func=pcap_command)


def pcap_command(args):
    analyzer = PcapAnalyzer(args.file)

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

    dispatch(
        OutputFormat.TABLE.value,
        table_data=(
            "PCAP Summary",
            ["Field", "Value"],
            rows,
        ),
    )