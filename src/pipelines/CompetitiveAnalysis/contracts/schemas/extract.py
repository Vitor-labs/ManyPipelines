"""
This module defines the main schemas for the extraction stage with
raw_complaint dataset
"""

from pandas import Timestamp
from pandera import DataFrameSchema, Column, Check, UInt, String, Bool

schema = DataFrameSchema(
    columns={
        "CMPLID": Column(
            dtype=UInt,
            unique=True,
            required=True,
            coerce=True,
            description="ID of the complaint on NHTSA",
            title="COMPLAINT ID",
        ),
        "ODINO": Column(
            dtype=UInt,
            unique=True,
            required=True,
            coerce=True,
            description="ODI number of the vehicle",
            title='VEHICLE "ODI" NUMBER',
        ),
        "MFR_NAME": Column(
            dtype=String,
            nullable=True,
            required=True,
            description="Name of the vehicle Manufacturer",
            title="MANUFACTURER NAME",
        ),
        "MAKETXT": Column(
            dtype=String,
            nullable=True,
            required=True,
            description="Name of the vehicle Make",
            title="MAKE NAME",
        ),
        "MODELTXT": Column(
            dtype=String,
            nullable=True,
            required=True,
            description="Name of the vehicle Model",
            title="MODEL NAME",
        ),
        "YEARTXT": Column(
            dtype=UInt,
            checks=[
                Check.between(min_value=1910, max_value=2030),
            ],
            nullable=True,
            required=True,
            coerce=True,
            description="Year of the vehicle fabrication",
            title="FABRICAITON YEAR",
        ),
        "CRASH": Column(
            dtype=Bool,
            coerce=True,
            required=True,
            description="Complaint related a Crash case",
        ),
        "FAILDATE": Column(
            dtype=UInt,
            required=True,
            coerce=True,
            description="Complaint failure dated in YYYYMMDD format",
            title="DATE OF FAILURE",
        ),
        "FIRE": Column(
            dtype=Bool,
            coerce=True,
            required=True,
            description="Complaint related a Fire start case",
        ),
        "INJURED": Column(
            dtype=UInt,
            checks=[Check.between(min_value=0, max_value=99)],
            coerce=True,
            required=True,
            description="Number of people injuried involved in the incident",
        ),
        "DEATHS": Column(
            dtype=UInt,
            checks=[Check.between(min_value=0, max_value=99)],
            coerce=True,
            required=True,
            description="Number of deaths involved in the incident",
        ),
        "COMPDESC": Column(
            dtype=String,
            nullable=True,
            required=True,
            description="Description of the problematic component (not reliable)",
            title="COMPONENT DESCRIPTION",
        ),
        "CITY": Column(
            dtype=String,
            nullable=True,
            required=True,
            description=None,
        ),
        "STATE": Column(
            dtype="object",
            required=True,
            description=None,
        ),
        "VIN": Column(
            dtype=String,
            nullable=True,
            required=True,
            description="Vehicle Identification Number",
        ),
        "DATEA": Column(
            # Name: DATEA, Length: 234488, dtype: int64" doesn't match format "%Y%m%d", at position 0.
            dtype="datetime64[ns]",
            checks=[
                Check.between(
                    min_value=Timestamp(19100101, tz="UTC"),
                    max_value=Timestamp(20301231, tz="UTC"),
                )
            ],
            coerce=True,
            required=True,
            description="Date when the complaint was added to NHTSA database in YYYYMMDD format",
            title="DATE ADDED",
        ),
        "LDATE": Column(
            dtype="datetime64[ns]",
            checks=[
                Check.between(
                    min_value=Timestamp(19100101, tz="UTC"),
                    max_value=Timestamp(20301231, tz="UTC"),
                )
            ],
            coerce=True,
            required=True,
            description="Date when the complaint was received by NHTSA in YYYYMMDD format",
            title="DATE RECEIVED",
        ),
        "MILES": Column(
            dtype=UInt,
            checks=[Check.greater_than_or_equal_to(min_value=0.0)],
            coerce=True,
            nullable=True,
            required=True,
            description="Total miles of the vehicle",
        ),
        "OCCURENCES": Column(
            dtype=UInt,
            checks=[
                Check.between(min_value=0.0, max_value=99.0),
            ],
            coerce=True,
            nullable=True,
            required=True,
            description="number of times that the problem occured",
        ),
        "CDESCR": Column(
            dtype=String,
            nullable=True,
            required=True,
            description="Complaint description",
            title="COMPLAINT TEXT",
        ),
        "CMPL_TYPE": Column(
            dtype=String,
            required=True,
            description="Complaint type",
            title="COMPLAINT TYPE",
        ),
        "POLICE_RPT_YN": Column(
            dtype=Bool,
            coerce=True,
            required=True,
            description="Police report on the incident",
            title="POLICE REPORT",
        ),
        "PURCH_DT": Column(
            dtype="datetime64[ns]",
            checks=[Check.greater_than_or_equal_to(min_value=19800101)],
            coerce=True,
            nullable=True,
            required=True,
            description="Date when the vehicle was purchased in YYYYMMDD format",
            title="PURCHASE DATE",
        ),
        "ORIG_OWER_YN": Column(
            dtype=Bool,
            coerce=True,
            nullable=True,
            required=True,
            description="Original owner of the vehicle",
            title="ORIGINAL OWNER",
        ),
        "ANTI_BRAKES_YN": Column(
            dtype=Bool,
            coerce=True,
            nullable=True,
            required=True,
            description="Vehicle has anti brakes",
            title="ANTI-LOCK BRAKES",
        ),
        "CRUISE_CONT_YN": Column(
            dtype=Bool,
            coerce=True,
            nullable=True,
            required=True,
            description="Vehicle has cruise control",
            title="CRUISE CONTROL",
        ),
        "NUM_CYLS": Column(
            dtype=UInt,
            checks=[
                Check.between(min_value=0.0, max_value=16.0),
            ],
            coerce=True,
            nullable=True,
            required=True,
            description="Number of cylinders, 0 to 16",
            title="NUMBER OF CYLINDERS",
        ),
        "DRIVE_TRAIN": Column(
            dtype=String,
            checks=[
                Check.isin(["2WD", "4WD", "AWD"]),
            ],
            nullable=True,
            required=True,
            title="DRIVE TRAIN",
        ),
        "FUEL_SYS": Column(
            dtype=String,
            checks=[
                Check.isin(["FI", "TB"]),
            ],
            nullable=True,
            required=True,
            title="FUEL SYSTEM",
        ),
        "FUEL_TYPE": Column(
            dtype=String,
            checks=[
                Check.isin(["BF", "CN", "DS", "GS", "HE"]),
            ],
            nullable=True,
            required=True,
        ),
        "TRASN_TYPE": Column(
            dtype=String,
            checks=[Check.isin(["AUTO", "MAN"])],
            nullable=True,
            required=True,
        ),
        "VEH_SPEED": Column(
            dtype=UInt,
            checks=[
                Check.greater_than_or_equal_to(min_value=0.0),
                Check.less_than_or_equal_to(max_value=999.0),
            ],
            coerce=True,
            nullable=True,
            required=True,
            description="Vehicle speed on the incident in miles per hour",
            title="VEHICLE SPEED",
        ),
        "DOT": Column(
            dtype=String,
            nullable=True,
            required=True,
            description="DEPARTMENT OF TRANSPORTATION TIRE IDENTIFIER",
        ),
        "TIRE_SIZE": Column(
            dtype=String,
            nullable=True,
            required=True,
        ),
        "LOC_OF_TIRE": Column(
            dtype=String,
            checks=[
                Check.isin(["FSW", "DSR", "FTR", "PSR", "SPR"]),
            ],
            nullable=True,
            required=True,
            description="LOCATION OF TIRE CODE",
        ),
        "TIRE_FAIL_TYPE": Column(
            dtype=String,
            checks=[
                Check.isin(["BST", "BLW", "TTL", "OFR", "TSW", "TTR", "TSP"]),
            ],
            nullable=True,
            required=True,
            description="TYPE OF TIRE FAILURE CODE",
        ),
        "ORIG_EQUIP_YN": Column(
            dtype=Bool,
            coerce=True,
            nullable=True,
            required=True,
            title="ORIGINAL EQUIPMENT",
        ),
        "MANUF_DT": Column(
            dtype="datetime64[ns]",
            coerce=True,
            nullable=True,
            required=True,
            title="DATE OF MANUFACTURE",
        ),
        "SEAT_TYPE": Column(
            dtype=String,
            checks=[
                Check.isin(["B", "C", "I", "IN", "TD"]),
            ],
            nullable=True,
            required=True,
            description="TYPE OF CHILD SEAT CODE",
        ),
        "RESTRAINT_TYPE": Column(
            dtype=String,
            checks=[Check.isin(["B", "A"])],
            nullable=True,
            required=True,
            description="RESTRAINT INSTALLATION SYSTEM CODE",
        ),
        "DEALER_NAME": Column(
            dtype=String,
            nullable=True,
            required=True,
            description=None,
            title=None,
        ),
        "DEALER_TEL": Column(
            dtype=String,
            nullable=True,
            required=True,
        ),
        "DEALER_CITY": Column(
            dtype=String,
            nullable=True,
            required=True,
        ),
        "DEALER_STATE": Column(
            dtype=String,
            nullable=True,
            required=True,
        ),
        "DEALER_ZIP": Column(
            dtype=String,
            nullable=True,
            required=True,
        ),
        "PROD_TYPE": Column(
            dtype=String,
            checks=[Check.isin(["V", "T", "E", "C"])],
            nullable=True,
            required=True,
            title="PRODUCT TYPE CODE",
        ),
        "REPAIRED_YN": Column(
            dtype=Bool,
            coerce=True,
            nullable=True,
            required=True,
            description="WAS DEFECTIVE TIRE REPAIRED",
        ),
        "MEDICAL_ATTN": Column(
            dtype=Bool,
            coerce=True,
            required=True,
        ),
        "VEHICLES_TOWED_YN": Column(
            dtype=Bool,
            coerce=True,
            nullable=True,
            required=True,
        ),
    },
    strict=False,
    name="RawComplaints",
    report_duplicates="all",
    title="Pre-Processed Complaints",
    description="Complaints dataset downloaded from NHTSA repository, no precessment step aplyed",
)
