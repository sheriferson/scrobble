from dataclasses import dataclass
from typing import Optional
from abc import ABC, abstractmethod

@dataclass
class Track(ABC):
    track_title: str
    track_artist: Optional[str]
    disc_no: Optional[int]
    track_position: int
    track_length: int

    def __str__(self):
        pass

    @property
    @abstractmethod
    def artist(self):
        pass
    def parse_source_result(cls, result: dict, dics_no: Optional[int] = 1):
        pass