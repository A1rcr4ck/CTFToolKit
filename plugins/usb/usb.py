from core.logger import success, error
from usb.keyboard import decode_file


def run(args):

    try:

        text = decode_file(args.file)

        success("Decoded Output\n")

        print(text)

    except Exception as e:

        error(str(e))