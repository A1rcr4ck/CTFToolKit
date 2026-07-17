from PIL import Image

from forensic.exif import ExifExtractor


def test_extract_image_information(tmp_path):

    image = tmp_path / "sample.jpg"

    Image.new("RGB", (200, 100)).save(image)

    result = ExifExtractor(image).extract()

    assert result["Format"] == "JPEG"
    assert result["Width"] == 200
    assert result["Height"] == 100
    assert result["Mode"] == "RGB"


def test_metadata_is_dictionary(tmp_path):

    image = tmp_path / "sample.jpg"

    Image.new("RGB", (100, 100)).save(image)

    result = ExifExtractor(image).extract()

    assert isinstance(result["Metadata"], dict)