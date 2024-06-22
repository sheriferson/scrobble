from abc import ABC

from typing import Optional
from scrobble.models.track import Track

class CD(ABC):
    id: str
    title: str
    artist: str
    year: Optional[str]
    discs: int
    tracks: Optional[list[Track]] = None
