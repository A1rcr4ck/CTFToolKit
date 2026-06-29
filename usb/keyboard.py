from pathlib import Path

from usb.hid import hid_to_char
from core.filetype import is_text, is_pcap



def decode_reports(reports):

    output = ""

    for report in reports:

        report = report.strip()

        if len(report) != 16:
            continue

        if report == "0000000000000000":
            continue

        modifier = int(report[0:2], 16)
        keycode = int(report[4:6], 16)

        if keycode == 0:
            continue

        char = hid_to_char(modifier, keycode)

        if char == "<BACKSPACE>":
            output = output[:-1]
            continue

        elif char == "<ENTER>":
            output += "\n"
            continue

        output += char

    return output


def decode_txt(filename):

    with open(filename) as f:
        reports = f.readlines()

    return decode_reports(reports)


def decode_pcap(filename):

    try:
        from usb.tshark import extract_hid_reports

        reports = extract_hid_reports(filename)

        return decode_reports(reports)

    except Exception:

        raise RuntimeError(
            "\nNo PCAP parser available.\n"
            "Install tshark or use extracted HID reports (.txt)."
        )


def decode_file(filename):

    if is_text(filename):
        return decode_txt(filename)

    if is_pcap(filename):
        return decode_pcap(filename)

    raise RuntimeError("Unsupported file type.")
