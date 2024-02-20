"""
This module defines the basic flow of data Tranformation from data
retrived from NHTSA.
"""

import logging
import os
import time
from datetime import date, datetime
from functools import lru_cache
from typing import Dict, FrozenSet, List

from src.drives.http_request import HttpRequest
from src.drives.interfaces.structure_dataset import (
    DatasetFlag,
    RecallDataset,
    RetrivedDataset,
    TransformedDataset,
    TransformedRecalls,
)
from src.errors.transform_error import TransformError
from src.stages.contracts.extract_contract import ExtractContract
from src.stages.contracts.transform_contract import TransformContract
from src.stages.utils.decorators import rate_limiter, retry
from src.stages.utils.logger import setup_logger


class DataTransformer:
    """
    Class to define the flow of the data transformation step

    methods:
        transform -> TransformContract: increase the dataset, adding columns
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.parts = (
            "door, window, windshield, wiper, glass, hood, trunk, moonroof, "
            + "bumper, tail light, pillar, undershield, roof rack, latch, he"
            + "adlight, door handle, door keypad, window, weatherstripping, "
            + "side mirror, lighting, swing gate, cowl grille, hard top, ski"
            + "d plate, sheet metal, running boards, water leak, etc"
        )
        setup_logger()

    def transform(
        self, contract: ExtractContract, flag: DatasetFlag
    ) -> TransformContract:
        """
        Main flow to tranform data colleted from previews steps

        Args:
            contract (ExtractContract): contract with raw data to transform
            flag (DatasetFlag): dataset typo

        Raises:
            TransformError: Error occouring during this flow

        Returns:
            TransformContract: contract with transformed data to the next step
        """
        start_time = time.time()
        self.logger.info("Running Transform stage")

        try:
            match flag.name:
                case "COMPLAINTS":
                    return TransformContract(
                        content=self.__transform_complaints(contract)
                    )
                case "RECALLS":
                    return TransformContract(content=self.__transform_recalls(contract))
                case _:
                    raise TransformError("Unknow type of Dataset Received.")

        except TransformError as exc:
            self.logger.exception(exc)
            raise exc

        finally:
            self.logger.info("--- %s minutes ---", round(time.time() - start_time, 2))

    def __transform_recalls(
        self, contract: ExtractContract
    ) -> List[TransformedRecalls]:
        """
        TODO: implement parallelism
        increments the dataset with addtional info:

        Args:
            contract (ExtractContract): dataset collected

        Returns:
            List[TransformedDataset]: list of dict, alike a pandas dataframe
        """
        extract_date: date = contract.extract_date
        extract_info: List[RecallDataset] = contract.raw_data
        transformed_data: List[TransformedRecalls] = []

        credentials = self.__load_classifier_credentials()

        def extract_url(text: str) -> str:
            start = text.find("https://")
            end = text.find(")", start)
            return text[start:end]

        def convert_float(text: str) -> float:
            try:
                return round(float(text), 2) if text != "" else 0.0
            except ValueError:
                return 0.0

        classes = self.__load_categories("Failures")

        text = (
            "Que"
            + "stion 1: According to the component and the decription, check"
            + " if the problem it's related to an external part of the car, "
            + f"body exterior, ({self.parts}). If yes, answer F8. Otherwise,"
            + "answer NOT F8. Question 2: For each of these sentences that y"
            + "our answer 1 was 'F8', check if it is related to only one of "
            + f"the following categories: {list(classes)}. Your answer must "
            + "be only one of these categories. Note: 'OWD' means 'opened wh"
            + "ile driving', it happens only when you read explictly that the vehi"
            + "cle is in motion AND the hood/door/trunk/liftgate/tailgate op"
            + "ened inadvertenly. Note 2: 'FELL OFF' only happens when somet"
            + "hing completely detached/flew off/came off. This kind of word"
            + " should be explicit. Don't consider glass broken, shattered, "
            + "cracked or exploded as FELL OFF. Note 3: LOOSE happens when t"
            + "here is something loosen, hanging or similar. This must be ex"
            + "plicit in the text. Don't consider glass broken, shattered, c"
            + "racked or exploded as LOOSE. If you cannot relate to any of t"
            + "he categories, answer NOT SURE. Answer me in the following fo"
            + "rmat: 'ANSWER 1~~~ANSWER 2'. If you cannot assist, all must b"
            + "e NA. You should be objective and cold. Each sentence must be"
            + " treated separately and indivdually in a different line, even"
            + " if all sentences are equal. NEVER change the answer format m"
            + "entioned."
        )
        for data_id, data in enumerate(extract_info):
            self.logger.debug("%s of %s", data_id, len(extract_info))

            data = {
                str(key): value
                for key, value in data.items()
                if str(key) in TransformedRecalls.__annotations__.keys()
            }
            prompt = (
                f'With this problematic component {str(data["COMPONENT"])} '
                f'and this decription: {str(data["RECALL_DESCRIPTION"])}. ' + text
            )
            function, _, failure = self.__classify_case(
                prompt,
                credentials["url"],
                credentials["token"],
            )
            info = TransformedRecalls(
                REPORT_RECEIVED_DATE=datetime.strptime(
                    str(data["REPORT_RECEIVED_DATE"]), "%m/%d/%Y"
                ),
                NHTSA_ID=str(data["NHTSA_ID"]),
                RECALL_LINK=extract_url(str(data["RECALL_LINK"])),
                MANUFACTURER=str(data["MANUFACTURER"]).replace('"', "").strip(),
                SUBJECT=str(data["SUBJECT"]).replace('"', "").strip(),
                COMPONENT=str(data["COMPONENT"]).replace('"', "").strip(),
                MFR_CAMPAIGN_NUMBER=str(data["MFR_CAMPAIGN_NUMBER"])
                .replace('"', "")
                .strip(),
                RECALL_TYPE=str(data["RECALL_TYPE"]).replace('"', "").strip(),
                POTENTIALLY_AFFECTED=int(str(data["POTENTIALLY_AFFECTED"])),
                RECALL_DESCRIPTION=str(data["RECALL_DESCRIPTION"])
                .replace('"', "")
                .strip(),
                CONSEQUENCE_SUMMARY=str(data["CONSEQUENCE_SUMMARY"])
                .replace('"', "")
                .strip(),
                CORRECTIVE_ACTION=str(data["CORRECTIVE_ACTION"])
                .replace('"', "")
                .strip(),
                PARK_OUTSIDE_ADVISORY=str(data["PARK_OUTSIDE_ADVISORY"]).strip().lower()
                == "yes",
                DO_NOT_DRIVE_ADVISORY=str(data["DO_NOT_DRIVE_ADVISORY"]).strip().lower()
                == "yes",
                COMPLETION_RATE=convert_float(str(data["COMPLETION_RATE"])),
                FUNCTION=function,
                FAILURE_MODE=failure,
                EXTRACTED_DATE=extract_date,
            )
            transformed_data.append(info)
        return transformed_data

    def __transform_complaints(
        self, contract: ExtractContract
    ) -> List[TransformedDataset]:
        """
        increments the dataset with addtional info:
            NEW_OLD: str
            FUNCTION: str -> ML Based (Binary Classification)
            COMPONET: str -> ML Based (Multi-Class Classification)
            FAILURE: str -> ML Based (Multi-Class Classification)
            FULL_STATE: str
            FAIL_QUARTER: str
            BINNING: str -> COMPONENT + FAILURE
            EXTRACTED_DATE: date

        Args:
            contract (ExtractContract): dataset collected

        Returns:
            List[TransformedDataset]: list of dict, alike a pandas dataframe
        """
        extract_date: date = contract.extract_date
        extract_info: List[RetrivedDataset] = contract.raw_data
        transformed_data: List[TransformedDataset] = []

        credentials = self.__load_classifier_credentials()
        categories = self.__load_categories("Binnings")

        text = (
            "Question 1: For this complaint, check if it is related to an ex"
            + f"ternal part of the car, body exterior, ({self.parts}). If ye"
            + "s, answer 'F8'. Otherwise, answer 'NOT F8'. Note that most of"
            + "the problems related to power liftgate electrical problems an"
            + "d rear view camera are NOT F8. Question 2: For each of these "
            + "sentences that your answer 1 was 'F8', check if it is related"
            + f"to only one of the following categories: {list(categories)}."
            + " You should give only one answer with one answer for Question"
            + " 1 and one answer for Question 2 in the following format: 'AN"
            + "SWER 1~~~ANSWER 2'. Note: 'OWD' means 'opened while driving' "
            + "and 'F&F' means 'fit and finish', for problems related to flu"
            + "shness and margin. Note 2: For model Escape (2020 forward), t"
            + "here is a common problem related to door check arm when the c"
            + "omplaint is related to the door making popping sounds, openin"
            + "g and closing problens, hinges and welds. If you cannot relat"
            + "e, answer NOT SURE. Answer in the correct order. If you canno"
            + "t assist, answer 1, and answer 2 must be NA. You should be ob"
            + "jective and cold. Never change the answer format mentioned."
        )
        for data_id, data in enumerate(extract_info):
            self.logger.debug("%s of %s", data_id, len(extract_info))

            def get_quarter(date_: str) -> str:
                if date_ in ("", " ", None) and len(date_) != 8:
                    return "~"
                date_obj = datetime.strptime(date_, "%Y%m%d")
                quarter = (date_obj.month - 1) // 3 + 1
                return f"{date_obj.year}Q{quarter}"

            function, component, failure = self.__classify_case(
                f"\"{data['CDESCR']}\" {text}", credentials["url"], credentials["token"]
            )
            binning = (
                f"{component} | {failure}"
                if component != "~" and failure != "~"
                else "~"
            )
            dataset: TransformedDataset = {
                **data,
                "FUNCTION": function,
                "COMPONET": component,
                "FAILURE": failure,
                "BINNING": binning,
                "FULL_STATE": self.__convert_code_into_state(str(data["STATE"])),
                "FAIL_QUARTER": get_quarter(str(data["FAILDATE"])),
                "EXTRACTED_DATE": extract_date,
            }  # type: ignore
            transformed_data.append(dataset)
        return transformed_data

    def __load_classifier_credentials(self) -> Dict[str, str]:
        """
        create a dict with classifier endpoint and auth.

        Returns:
            Dict[str, str]: _description_
        """
        credentials = {}

        credentials["url"] = str(os.getenv("API_ENDPOINT"))

        credentials["token"] = HttpRequest(
            str(os.getenv("TOKEN_ENDPOINT"))
        ).request_token(
            id_=str(os.getenv("CLIENT_ID")),
            secret=str(os.getenv("CLIENT_SECRET")),
            scope=str(os.getenv("SCOPE")),
        )
        return credentials

    @retry([Exception])
    @rate_limiter(70, 1)
    @lru_cache(maxsize=70)
    def __classify_case(
        self,
        text: str,
        url: str,
        token: str,
    ) -> List[str]:
        """
        Uses ChatGPT-4.0 to classify each recall by failure mode

        Args:
            decription (str): complaint description
            url (str): api endpoint
            token (str): authorization token

        Raises:
            exc: ConnectionError, API not responded

        Returns:
            str: result of classificaiton (failure mode)
        """
        content = {
            "model": "gpt-4",
            "context": (
                "You are a helpful text reader and analyzer. You need to give me 2 answers."
                + text
            ),  # sets the overall behavior of the assistant.
            "messages": [{"role": "user", "content": text}],
            "parameters": {
                "temperature": 0.05,  # Determines the randomnes of the model's response.
            },
        }
        try:
            response = HttpRequest.call_external_api(url, token, content)
        except Exception as exc:
            self.logger.exception(exc)
            self.logger.error(exc)
            raise TransformError(str(exc)) from Exception

        if response["status_code"] == 200:
            return self.__process_response(str(response["message"]))

        return ["NOT CLASSIFIED", "~", "~"]

    def __process_response(self, message: str) -> List[str]:
        """
        Process response from ChatGPT, divide function, component and failure mode
        response format is: "Function~~~Result" where result is "component | failure"

        Args:
            data (str): api response message

        Returns:
            List[str | float]: function, component, failure
        """
        if "\n" in message:
            message = message.split("\n")[0]

        if len(parts := message.split("~~~")) == 2:
            function, result = parts

            if function == "NOT F8":
                return [function, "~", "~"]

            if function == "F8":
                if "|" not in result:  # case where recalls is being processed
                    return [function, "~", result]

                component, failure = result.split(" | ")
                return [function, component, failure]
        print(message)
        return ["NOT CLASSIFIED", "~", "~"]

    def __convert_code_into_state(self, state_code: str) -> str:
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

    def __load_categories(self, flag: str) -> FrozenSet[str]:
        """
        Loads categories for classification based on a flag

        Args:
            flag (str): describes which type of categories return

        Returns:
            List[str]: categories filtered by flag
        """
        categories = []
        with open("./data/external/binnings.txt", encoding="utf-8", mode="r") as file:
            for line in file.readlines():
                if flag == "Binnings":
                    categories.append(line.strip("\n"))
                if flag == "Failures":
                    if line.find("|") == -1:
                        continue
                    categories.append(line.split(" | ")[1].strip("\n"))
                if flag == "Components":
                    categories.append(line.split(" | ")[0])

        return frozenset(categories)
