import subprocess


def extract_hid_reports(filename):
    """
    Extract USB HID reports from a PCAP using Tshark.
    Returns a list of HID report strings.
    """

    command = [
        "tshark",
        "-r",
        filename,
        "-T",
        "fields",
        "-e",
        "usb.capdata"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    reports = []

    for line in result.stdout.splitlines():

        line = line.strip()

        if line:
            reports.append(line)

    return reports