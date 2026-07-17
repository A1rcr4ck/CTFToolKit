from pathlib import Path

from PIL import Image
from PIL.ExifTags import TAGS


class ExifExtractor:

    def __init__(self, file_path):

        self.file_path = Path(file_path)

    def extract(self):

        image = Image.open(self.file_path)

        exif = image.getexif()

        metadata = {}

        if exif:

            for tag_id, value in exif.items():

                tag = TAGS.get(tag_id, str(tag_id))

                metadata[tag] = str(value)

        return {
            "File": self.file_path.name,
            "Format": image.format,
            "Mode": image.mode,
            "Width": image.width,
            "Height": image.height,
            "Metadata": metadata,
        }