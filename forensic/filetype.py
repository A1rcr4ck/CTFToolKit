from pathlib import Path


MAGIC_SIGNATURES = [
    (b"\x7FELF", "ELF Executable"),
    (b"MZ", "PE Executable"),
    (b"%PDF-", "PDF Document"),
    (b"\x89PNG\r\n\x1A\n", "PNG Image"),
    (b"\xFF\xD8\xFF", "JPEG Image"),
    (b"GIF87a", "GIF Image"),
    (b"GIF89a", "GIF Image"),
    (b"BM", "BMP Image"),
    (b"PK\x03\x04", "ZIP Archive"),
    (b"PK\x05\x06", "ZIP Archive"),
    (b"PK\x07\x08", "ZIP Archive"),
    (b"\x1F\x8B", "GZIP Archive"),
    (b"7z\xBC\xAF\x27\x1C", "7-Zip Archive"),
    (b"Rar!\x1A\x07\x00", "RAR Archive"),
    (b"Rar!\x1A\x07\x01\x00", "RAR v5 Archive"),
]


class FileTypeDetector:

    def __init__(self, file_path):

        self.file_path = Path(file_path)

    def detect(self):

        with self.file_path.open("rb") as f:
            header = f.read(32)

        for signature, description in MAGIC_SIGNATURES:
            if header.startswith(signature):
                return {
                    "File": self.file_path.name,
                    "Type": description,
                    "Signature": signature.hex().upper(),
                }

        return {
            "File": self.file_path.name,
            "Type": "Unknown",
            "Signature": header[:8].hex().upper(),
        }