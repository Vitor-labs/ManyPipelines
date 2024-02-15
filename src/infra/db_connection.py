"""
This module implements a basic connetion to a local database in sqlite3 to manage
weekly reports from this pipeline.
TODO: change the connetion to a CloudSQL postgress instance.
"""

import os
import sqlite3
from sqlite3.dbapi2 import Connection as LocalConn

import psycopg2  # pylint: disable=E0401
from psycopg2.extensions import connection as Connection  # pylint: disable=E0401


class DBConnector:
    """
    Represents a connector for the database. implements both connection
    to local sqlite and cloudSQL postgres databases.
    TODO: remove sqlite connection after cloud infrasctructure ends.
    """

    local: LocalConn
    conn: Connection

    @classmethod
    def connect_cloud(cls) -> None:
        """
        Establishes a connection to the PostgreSQL database.

        Raises:
            psycopg2.OperationalError: If the connection fails.
        """
        try:
            print("Connecting to DataBase...", end=" ")
            cls.conn = psycopg2.connect(
                database=os.getenv("DATABASE"),
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
            )
            if cls.conn:
                print("Connected !")

        except psycopg2.OperationalError as exc:
            raise exc

    @classmethod
    def connect_local(cls) -> None:
        """
        Establishes a connection to the local sqlite database.
        """
        try:
            print("local database connection in process...", end=" ")
            cls.local = sqlite3.connect("nhtsa_data.sqlite3")
            if cls.__assure_database_exists():
                print("Database sync... Continuing")
            else:
                print("No table exists. Tables complaints and recalls Created")
                with cls.local as connect:
                    connect.cursor().execute(
                        """
                        CREATE TABLE IF NOT EXISTS complaints (
                            CMPLID TEXT PRIMARY KEY,
                            ODINO TEXT,
                            MFR_NAME TEXT,
                            MAKETXT TEXT,
                            MODELTXT TEXT,
                            YEARTXT TEXT,
                            CRASH INTEGER,
                            FAILDATE TEXT,
                            FIRE INTEGER,
                            INJURED INTEGER,
                            DEATHS INTEGER,
                            COMPDESC TEXT,
                            CITY TEXT,
                            STATE_ TEXT,
                            VIN TEXT,
                            DATEA TEXT,
                            LDATE TEXT,
                            MILES INTEGER,
                            OCCURENCES INTEGER,
                            CDESCR TEXT,
                            CMPL_TYPE TEXT,
                            POLICE_RPT_YN INTEGER,
                            PURCH_DT TEXT,
                            ORIG_OWER_YN INTEGER,
                            ANTI_BRAKES_YN INTEGER,
                            CRUISE_CONT_YN INTEGER,
                            NUM_CYLS INTEGER,
                            DRIVE_TRAIN TEXT,
                            FUEL_SYS TEXT,
                            FUEL_TYPE TEXT,
                            TRASN_TYPE TEXT,
                            VEH_SPEED INTEGER,
                            DOT TEXT,
                            TIRE_SIZE TEXT,
                            LOC_OF_TIRE TEXT,
                            TIRE_FAIL_TYPE TEXT,
                            ORIG_EQUIP_YN INTEGER,
                            MANUF_DT TEXT,
                            SEAT_TYPE TEXT,
                            RESTRAINT_TYPE TEXT,
                            DEALER_NAME TEXT,
                            DEALER_TEL TEXT,
                            DEALER_CITY TEXT,
                            DEALER_STATE TEXT,
                            DEALER_ZIP TEXT,
                            PROD_TYPE TEXT,
                            REPAIRED_YN INTEGER,
                            MEDICAL_ATTN INTEGER,
                            VEHICLES_TOWED_YN INTEGER,
                            FUNCTION_ TEXT,
                            COMPONET TEXT,
                            FAILURE TEXT,
                            BINNING TEXT,
                            FULL_STATE TEXT,
                            FAIL_QUARTER TEXT,
                            Full_VIN TEXT,
                            Production_Date TEXT,
                            VFG TEXT,
                            Char_10_MY TEXT,
                            Char_11_Plant TEXT,
                            Char_8_Engine TEXT,
                            Vehicle_Line_WERS TEXT,
                            Vehicle_Line_GSAR TEXT,
                            Vehicle_Line_Global TEXT,
                            Assembly_Plant TEXT,
                            Warranty_Start_Date TEXT,
                            Repair_Date_1 TEXT,
                            Repair_Date_2 TEXT,
                            EXTRACTED_DATE TEXT
                        );
                        """
                    )
                    connect.cursor().execute(
                        """
                        CREATE TABLE IF NOT EXISTS complaints (
                            NHTSA_ID TEXT PRIMARY KEY,
                            REPORT_RECEIVED_DATE TEXT,
                            RECALL_LINK TEXT,
                            MANUFACTURER TEXT,
                            SUBJECT TEXT,
                            COMPONENT TEXT,
                            MFR_CAMPAIGN_NUMBER TEXT,
                            RECALL_TYPE TEXT,
                            POTENTIALLY_AFFECTED INTEGER,
                            RECALL_DESCRIPTION TEXT,
                            CONSEQUENCE_SUMMARY TEXT,
                            CORRECTIVE_ACTION TEXT,
                            PARK_OUTSIDE_ADVISORY TEXT,
                            DO_NOT_DRIVE_ADVISORY TEXT,
                            COMPLETION_RATE REAL
                        );
                        """
                    )
            DBConnector.local.commit()

        except sqlite3.IntegrityError as exc:
            raise exc
        except sqlite3.OperationalError as exc:
            raise exc

    @classmethod
    def __assure_database_exists(cls) -> bool:
        """
        Asures that the necessary tables exists in database

        Returns:
            bool: true if exists else false. Also create all tables needed
        """
        query = (
            "SELECT name FROM sqlite_master WHERE name='complaints' OR name='recalls';"
        )
        cursor = DBConnector.local.cursor()
        response = cursor.execute(query)

        if response.fetchone() is None:
            return False

        return True
