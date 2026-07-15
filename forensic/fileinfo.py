from datetime import datetime
from pathlib import Path


class FileInfo:

    def __init__(self, file_path):
        self.path = Path(file_path)
        self.stat = self.path.stat()

    @staticmethod
    def _format_size(size):

        units = ["B", "KB", "MB", "GB", "TB"]

        value = float(size)

        for unit in units:

            if value < 1024 or unit == units[-1]:
                return f"{value:.2f} {unit}"

            value /= 1024

    def info(self):

        return {
            "Name": self.path.name,
            "Extension": self.path.suffix,
            "Size": self._format_size(self.stat.st_size),
            "Size (Bytes)": self.stat.st_size,
            "Created": datetime.fromtimestamp(
                self.stat.st_ctime
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "Modified": datetime.fromtimestamp(
                self.stat.st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "Absolute Path": str(self.path.resolve()),
        }