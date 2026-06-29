from usb.tshark import extract_hid_reports

reports = extract_hid_reports("tests/keyboard.pcap")

print(f"Found {len(reports)} HID reports")

print()

for report in reports[:10]:
    print(report)