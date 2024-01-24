from scrobble.barcode_scanner import read_barcode

def test_read_barcode():
    test_image_path = 'tests/resources/CD1-600.jpeg'
    assert read_barcode(test_image_path) == '826257008428'