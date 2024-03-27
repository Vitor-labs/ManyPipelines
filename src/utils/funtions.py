"""
This module defines 
"""

import os
import sqlite3
from datetime import datetime
from typing import FrozenSet, Dict

from httpx import (
    AsyncHTTPTransport,
    Client,
    AsyncClient,
    HTTPTransport,
    Limits,
    Proxy,
    Timeout,
    HTTPStatusError,
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
        "C-MAX HYBRID": "C-MAX",
        "C-MAX ENERGI": "C-MAX",
        "E-150": "E-SERIES",
        "E-250": "E-SERIES",
        "E-350": "E-SERIES",
        "E-450": "E-SERIES",
        "F-250": "SUPERDUTY",
        "F-350": "SUPERDUTY",
        "F-350 SD": "SUPERDUTY",
        "F-450": "SUPERDUTY",
        "F-450 SD": "SUPERDUTY",
        "F-550": "SUPERDUTY",
        "F-550 SD": "SUPERDUTY",
        "F53": "F-53",
        "MKC": "CORSAIR / MKC",
        "MKS": "CONTINENTAL / MKS",
        "MKT": "AVIATOR / MKT",
        "MKX": "NAUTILUS / MKX",
        "MKZ": "ZEPHYR / MKZ",
        "ESCAPE HYBRID": "ESCAPE",
        "FUSION ENERGI": "FUSION",
        "MILAN HYBRID": "MILAN",
        "CONTINENTAL": "CONTINENTAL / MKS",
        "TRANSIT CONNECT": "TRANSIT CONNECT",
        "EXPLORER SPORT": "EXPLORER",
        "EXPLORER SPORT TRAC": "EXPLORER",
        "MOUNTAINEER": "MOUNTAINEER",
        "CORSAIR": "CORSAIR / MKC",
        "NAUTILUS": "NAUTILUS / MKX",
        "AVIATOR": "AVIATOR / MKT",
        "ZEPHYR": "ZEPHYR / MKZ",
        "SUPERDUTY SD": "SUPERDUTY",
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
    Reads the 'Dim_VinInfo' table from database and returns a dictionary
    with the primary keys (Full Vins) and all values of the column "ODINO".

    Returns:
        Dict[str, str]: dict with odino as key and full vin as value
    """
    try:
        with sqlite3.connect("your_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID, ODINO FROM Dim_VinInfo")
            rows = cursor.fetchall()
            results = {}

            for row in rows:
                vin, odino = row
                results[odino] = vin

            return results

    except sqlite3.DatabaseError as exc:
        print(f"Database error: {exc}")
        raise exc


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


def get_state_names() -> Dict[str, str]:
    """
    mapping of states codes and names

    Returns:
        Dict[str, str]: dict with mapping
    """
    return {
        "AK": "NA-USA-AK",
        "AL": "NA-USA-AL",
        "AR": "NA-USA-AR",
        "AZ": "NA-USA-AZ",
        "CA": "NA-USA-CA",
        "CO": "NA-USA-CO",
        "CT": "NA-USA-CT",
        "DC": "NA-USA-DC",
        "DE": "NA-USA-DE",
        "FL": "NA-USA-FL",
        "GA": "NA-USA-GA",
        "HI": "NA-USA-HI",
        "IA": "NA-USA-IA",
        "ID": "NA-USA-ID",
        "IL": "NA-USA-IL",
        "IN": "NA-USA-IN",
        "KS": "NA-USA-KS",
        "KY": "NA-USA-KY",
        "LA": "NA-USA-LA",
        "MA": "NA-USA-MA",
        "MD": "NA-USA-MD",
        "ME": "NA-USA-ME",
        "MI": "NA-USA-MI",
        "MN": "NA-USA-MN",
        "MO": "NA-USA-MO",
        "MS": "NA-USA-MS",
        "MT": "NA-USA-MT",
        "NC": "NA-USA-NC",
        "ND": "NA-USA-ND",
        "NE": "NA-USA-NE",
        "NH": "NA-USA-NH",
        "NJ": "NA-USA-NJ",
        "NM": "NA-USA-NM",
        "NV": "NA-USA-NV",
        "NY": "NA-USA-NY",
        "OH": "NA-USA-OH",
        "OK": "NA-USA-OK",
        "OR": "NA-USA-OR",
        "PA": "NA-USA-PA",
        "RI": "NA-USA-RI",
        "SC": "NA-USA-SC",
        "SD": "NA-USA-SD",
        "TN": "NA-USA-TN",
        "TX": "NA-USA-TX",
        "UT": "NA-USA-UT",
        "VA": "NA-USA-VA",
        "VT": "NA-USA-VT",
        "WA": "NA-USA-WA",
        "WI": "NA-USA-WI",
        "WV": "NA-USA-WV",
        "WY": "NA-USA-WY",
    }


def load_categories() -> FrozenSet[str]:
    """
    Accesses the 'Dim_Problems' table and selects all values from the
    'BINNING' column where the 'FUNCTION_' column value is 'F3'.
    TODO: change to Cloud SQL when deployed

    Returns:
        FrozenSet[str]: categories values that match the criteria.
    """
    try:
        with sqlite3.connect("your_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT BINNING FROM Dim_Problems WHERE FUNCTION_ = 'F3'")
            rows = cursor.fetchall()

        return frozenset([row[0] for row in rows])

    except sqlite3.DatabaseError as exc:
        print(f"Database error: {exc}")
        raise exc


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
        Dict[str, str]: dict with url and token if reponse status code is 200
    """
    try:
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
            response.raise_for_status()
    except HTTPStatusError as exc:
        raise exc

    return {
        "url": str(os.getenv("API_ENDPOINT")),
        "token": response.json()["access_token"],
    }
