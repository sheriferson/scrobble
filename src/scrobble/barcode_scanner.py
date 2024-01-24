from cv2 import barcode, imread
from typing import Optional


def read_barcode(imgpath: str) -> Optional[str]:
    bd = barcode.BarcodeDetector()
    return bd.detectAndDecode(imread(imgpath))[0]