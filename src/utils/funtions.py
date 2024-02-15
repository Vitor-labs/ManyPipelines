"""
This module defines 
"""

from datetime import datetime
from typing import FrozenSet, Dict


def get_quarter(date_: str) -> str:
    """
    Transforms the failure date into the quarter of the year

    Args:
        date_ (str): Failure Date

    Returns:
        str: Quarter of year of failure.
    """
    if date_ in ("", " ", None) and len(date_) != 8:
        return "~"
    date_obj = datetime.strptime(date_, "%Y%m%d")
    quarter = (date_obj.month - 1) // 3 + 1
    return f"Q{quarter}"


def get_mileage_class(miles: int) -> str:
    """
    Classify the case by miles of the car.

    Args:
        miles (int): Car miles.

    Returns:
        str: Car miles classfication.
    """
    if miles == 0:
        return "~"
    if 0 < miles < 6000:
        return "< 6k"
    if 6000 < miles < 12000:
        return "6K to 12K"
    if 12000 < miles < 18000:
        return "12K to 18K"
    if 18000 < miles < 24000:
        return "18K to 24K"
    if 24000 < miles < 30000:
        return "24K to 30K"
    return "> 36K"


def classify_binning(binning: str) -> str:
    """
    Transform the binning into the general failure mode.

    Args:
        binning (str): complaint classification

    Returns:
        str: failure mode
    """
    if "LOOSE" in binning:
        return "LOOSEN"
    if "FELL OFF" in binning:
        return "FELL OFF"
    if "DETACHED" in binning:
        return "FELL OFF"
    if "MOONROOF GLASS | CRACKED" in binning:
        return "Moonroof Glass Cracked/Exploded"
    if "MOONROOF GLASS | EXPLODED" in binning:
        return "Moonroof Glass Cracked/Exploded"
    if "FRONT WIPER | TOTALLY INOPERATIVE" in binning:
        return "Front Wiper Not Working"
    if "OWD" in binning:
        return "Latch OWD"
    return ""


def convert_code_into_state(state_code: str) -> str:
    """
    Converts state acronim into state full name

    Args:
        state_code (str): two letters state acronim

    Returns:
        str: State complete name
    """
    try:
        if state_code.isnumeric():
            return "~"
        states = {
            "Alabama": "AL",
            "Alaska": "AK",
            "Arizona": "AZ",
            "Arkansas": "AR",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "Delaware": "DE",
            "District of Columbia": "DC",
            "Florida": "FL",
            "Georgia": "GA",
            "Hawaii": "HI",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Iowa": "IA",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Maine": "ME",
            "Maryland": "MD",
            "Massachusetts": "MA",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Mississippi": "MS",
            "Missouri": "MO",
            "Montana": "MT",
            "Nebraska": "NE",
            "Nevada": "NV",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "New York": "NY",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Vermont": "VT",
            "Virginia": "VA",
            "Washington": "WA",
            "West Virginia": "WV",
            "Wisconsin": "WI",
            "Wyoming": "WY",
            "American Samoa": "AS",
            "Federated States of Micronesia": "FM",
            "Guam": "GU",
            "Marshall Islands": "MH",
            "Commonwealth of the Northern Mariana Islands": "MP",
            "Palau": "PW",
            "Puerto Rico": "PR",
            "U.S. Minor Outlying Islands": "M",
            "U.S. Virgin Islands": "VI",
        }
        if state_code not in states.values():
            return "~"
        return [k for k, v in states.items() if v == state_code][0]

    except KeyError:
        return "~"


def load_categories(flag: str = "Binnings") -> FrozenSet[str]:
    """
    Loads categories for classification based on a flag

    Args:
        flag (str): describes which type of categories return. Default to Binnings

    Returns:
        List[str]: categories filtered by flag
    """
    if flag not in {"Binnings", "Failures", "Components"}:
        raise ValueError(
            f"Invalid flag '{flag}' provided. Use only  'Binnings', 'Failures', 'Component'."
        )

    categories = set()
    with open("./data/external/binnings.txt", encoding="utf-8", mode="r") as file:
        for line in file.readlines():
            binning = line.split(",")[1]
            if flag == "Binnings":
                categories.add(binning.strip("\n"))
            if flag == "Failures":
                if "|" not in binning:
                    continue
                categories.add(binning.split(" | ")[1].strip("\n"))
            if flag == "Components":
                categories.add(binning.split(" | ")[0])

    return frozenset(categories)


def load_vfgs() -> Dict[str, str]:
    """
    loads vfg categories in memory for complaints transformations

    Raises:
        exc: FileNotFound Error

    Returns:
        Dict[str, str]: dict with unique binning as key and general vfg as value
    """
    vfgs = {}
    try:
        with open("./data/external/binnings.txt", encoding="utf-8", mode="r") as file:
            for line in file.readlines():
                VFG, binning = line.split(",")
                vfgs.update({binning: VFG})

    except FileNotFoundError as exc:
        raise exc

    return vfgs


def extract_url(text: str) -> str:
    """
    Extracts only the url part of a longer string

    Args:
        text (str): text string with a url inside

    Returns:
        str: only url part of the string
    """
    start = text.find("https://")
    end = text.find(")", start)
    return text[start:end]


def convert_float(text: str) -> float:
    """
    converts a text string into a 2 decimal cases float

    Args:
        text (str): number as string

    Returns:
        float: number converted
    """
    try:
        return round(float(text), 2) if text != "" else 0.0
    except ValueError:
        return 0.0
