from dataclasses import dataclass
from typing import Union


@dataclass
class BandMember:
    """
    Band Member data for output
    """
    first_name: Union[str, None] = None
    family_name: Union[str, None] = None
    instrument: Union[str, None] = None
