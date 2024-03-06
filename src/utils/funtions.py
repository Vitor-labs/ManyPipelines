"""
This module defines 
"""

import os
from datetime import datetime
from typing import FrozenSet, Dict

import pandas as pd
from httpx import (
    AsyncHTTPTransport,
    Client,
    AsyncClient,
    HTTPTransport,
    Limits,
    Proxy,
    Timeout,
)


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
    date_obj = datetime.strptime(str(date_), "%Y%m%d")
    quarter = (date_obj.month - 1) // 3 + 1
    return f"Q{quarter}"


def load_new_models() -> Dict[str, str]:
    """
    new vehicle models names for sheet f8

    Returns:
        Dict[str, str]: dict for replacement
    """
    return {
        "ESCAPE HYBRID": "ESCAPE",
        "C-MAX HYBRID": "C-MAX",
        "MILAN HYBRID": "MILAN",
        "EXPLORER SPORT": "EXPLORER",
        "EXPLORER SPORT TRAC": "EXPLORER",
        "FUSION ENERGI": "FUSION",
        "C-MAX ENERGI": "C-MAX",
        "F-250": "SUPERDUTY",
        "F-350": "SUPERDUTY",
        "F-350 SD": "SUPERDUTY",
        "F-450": "SUPERDUTY",
        "F-450 SD": "SUPERDUTY",
        "F-550": "SUPERDUTY",
        "F-550 SD": "SUPERDUTY",
        "SUPERDUTY SD": "SUPERDUTY",
        "F53": "F-53",
        "CORSAIR": "CORSAIR / MKC",
        "MKC": "CORSAIR / MKC",
        "ZEPHYR": "ZEPHYR / MKZ",
        "MKZ": "ZEPHYR / MKZ",
        "NAUTILUS": "NAUTILUS / MKX",
        "MKX": "NAUTILUS / MKX",
        "AVIATOR": "AVIATOR / MKT",
        "MKT": "AVIATOR / MKT",
        "CONTINENTAL": "CONTINENTAL / MKS",
        "MKS": "CONTINENTAL / MKS",
        "E-150": "E-SERIES",
        "E-250": "E-SERIES",
        "E-350": "E-SERIES",
        "E-450": "E-SERIES",
        # Include the replacements to correct potential duplicated replacements
        "CORSAIR / CORSAIR / MKC": "CORSAIR / MKC",
        "ZEPHYR / ZEPHYR / MKZ": "ZEPHYR / MKZ",
        "NAUTILUS / NAUTILUS / MKX": "NAUTILUS / MKX",
        "AVIATOR / AVIATOR / MKT": "AVIATOR / MKT",
        "CONTINENTAL / CONTINENTAL / MKS": "CONTINENTAL / MKS",
        "EXPLORER TRAC": "EXPLORER",
    }


def load_full_vins() -> Dict[str, str]:
    """
    Loads newest full vins.

    Returns:
        Dict[str, str]: dict with odino as key and full vin as value
    """
    df = pd.read_excel("./data/external/NSCCV-000502-20240304.xlsx", sheet_name="VOQS")
    df.dropna(inplace=True)
    df = df[~df["VIN"].str.endswith("*") & (df["VIN"] != "") & (df["VIN"] != "N/A")]

    voq_dict = df.set_index("ODI_ID")["VIN"].to_dict()
    return voq_dict


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


def create_client() -> Client:
    """
    Creates a common client for future http requests

    Returns:
        Client: client with ford proxies
    """
    ford_proxy = str(os.getenv("FORD_PROXY"))
    timeout_config = Timeout(10.0, connect=5.0)
    proxy_mounts = {
        "http://": HTTPTransport(proxy=Proxy(ford_proxy)),
        "https://": HTTPTransport(proxy=Proxy(ford_proxy)),
    }
    return Client(
        timeout=timeout_config,
        mounts=proxy_mounts,
        verify=False,
    )


def create_async_client() -> AsyncClient:
    """
    Creates a common client for future http requests

    Returns:
        Client: client with ford proxies
    """
    limits = Limits(max_connections=8)
    ford_proxy = Proxy(str(os.getenv("FORD_PROXY")))
    timeout_config = Timeout(10.0, connect=5.0, pool=4.0)
    proxy_mounts = {
        "http://": AsyncHTTPTransport(proxy=ford_proxy, limits=limits, retries=3),
        "https://": AsyncHTTPTransport(proxy=ford_proxy, limits=limits, retries=3),
    }
    return AsyncClient(
        timeout=timeout_config,
        mounts=proxy_mounts,
        verify=False,
    )


def load_classifier_credentials() -> Dict[str, str]:
    """
    create a dict with classifier endpoint and auth.

    Returns:
        Dict[str, str]: _description_
    """
    with create_client() as client:
        response = client.post(
            str(os.getenv("TOKEN_ENDPOINT")),
            data={
                "client_id": str(os.getenv("CLIENT_ID")),
                "client_secret": str(os.getenv("CLIENT_SECRET")),
                "scope": str(os.getenv("SCOPE")),
                "grant_type": "client_credentials",
            },
            timeout=160,
        )
    return {
        "url": str(os.getenv("API_ENDPOINT")),
        "token": response.json()["access_token"],
    }
