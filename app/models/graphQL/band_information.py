from dataclasses import dataclass
from typing import Union, List

from app.models.graphQL.band_member import BandMember


@dataclass
class BandInformation:
    """
    All Band data for output
    """
    band_id: Union[int, None] = None
    name: Union[str, None] = None
    genre: Union[str, None] = None
    band_members: Union[List[BandMember], None] = None
