from pathlib import Path
import gzip
import tarfile
import zipfile


class ArchiveInspector:

    def __init__(self, file_path):

        self.file_path = Path(file_path)

    def inspect(self):

        if zipfile.is_zipfile(self.file_path):
            return self._inspect_zip()

        if tarfile.is_tarfile(self.file_path):
            return self._inspect_tar()

        if self.file_path.suffix.lower() == ".gz":
            return self._inspect_gzip()

        raise ValueError("Unsupported archive format.")

    def _inspect_zip(self):

        with zipfile.ZipFile(self.file_path) as archive:

            files = []

            for info in archive.infolist():

                files.append(
                    {
                        "Name": info.filename,
                        "Original Size": info.file_size,
                        "Compressed Size": info.compress_size,
                        "Modified": "%04d-%02d-%02d %02d:%02d:%02d"
                        % info.date_time,
                    }
                )

        return {
            "File": self.file_path.name,
            "Archive Type": "ZIP",
            "File Count": len(files),
            "Files": files,
        }

    def _inspect_tar(self):

        with tarfile.open(self.file_path) as archive:

            files = []

            for member in archive.getmembers():

                files.append(
                    {
                        "Name": member.name,
                        "Original Size": member.size,
                        "Compressed Size": "-",
                        "Modified": member.mtime,
                    }
                )

        return {
            "File": self.file_path.name,
            "Archive Type": "TAR",
            "File Count": len(files),
            "Files": files,
        }

    def _inspect_gzip(self):

        with gzip.open(self.file_path, "rb") as gz:

            data = gz.read()

        return {
            "File": self.file_path.name,
            "Archive Type": "GZIP",
            "File Count": 1,
            "Files": [
                {
                    "Name": self.file_path.stem,
                    "Original Size": len(data),
                    "Compressed Size": self.file_path.stat().st_size,
                    "Modified": "-",
                }
            ],
        }