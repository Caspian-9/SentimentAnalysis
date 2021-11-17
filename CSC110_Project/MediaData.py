"""
media data
"""

from dataclasses import dataclass
import datetime


@dataclass
class ScrapedData:
    """
    Instance Attributes:
        - pub_date: publication date of scraped data
        - data: data scraped from online

    Representation Invariants:
        -
    """
    pub_date: datetime.date
    data: str    # subject to change depending on contents of json file
