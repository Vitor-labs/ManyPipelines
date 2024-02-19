### COMPLAINTS
```python
{
    'CMPLID': 1958584,
    'ODINO': 11566568,
    'MFR_NAME': 'Ford Motor Company',
    'MAKETXT': 'FORD',
    'MODELTXT': 'EXPEDITION',
    'YEARTXT': 2011,
    'CRASH': 'N',
    'FAILDATE': 20221205,
    'FIRE': 'N',
    'INJURED': 0,
    'DEATHS': 0,
    'COMPDESC': 'LATCHES/LOCKS/LINKAGES',
    'CITY': 'Crete',
    'STATE': 'IL',
    'VIN': '1FMJU2A51BE',
    'DATEA': 20240119,
    'LDATE': 20240119,
    'MILES': 115000.0,
    'OCCURENCES': nan,
    'CDESCR': 'The contact owns a 2011 Ford Expedition. The contact stated that the locking assembly on the driver’s side door was frozen and failed to operate as designed. Due to the issue, the contact was unable to enter the vehicle without using a hair dryer to warm up the lock. However, once the door was opened, the door was unable to close until the lock was heated up again. No warning lights illuminated.  The vehicle was not taken to the dealer and was not repaired. The manufacturer was notified of the failure and referred the contact to the NHTSA Hotline. The approximate failure mileage was 115,000.',
    'CMPL_TYPE': 'EVOQ',
    'POLICE_RPT_YN': 'N',
    'PURCH_DT': nan,
    'ORIG_OWER_YN': 'N',
    'ANTI_BRAKES_YN': 'N',
    'CRUISE_CONT_YN': 'N',
    'NUM_CYLS': nan,
    'DRIVE_TRAIN': nan,
    'FUEL_SYS': nan,
    'FUEL_TYPE': nan,
    'TRASN_TYPE': nan,
    'VEH_SPEED': nan,
    'DOT': nan,
    'TIRE_SIZE': nan,
    'LOC_OF_TIRE': nan,
    'TIRE_FAIL_TYPE': nan,
    'ORIG_EQUIP_YN': nan,
    'MANUF_DT': nan,
    'SEAT_TYPE': nan,
    'RESTRAINT_TYPE': nan,
    'DEALER_NAME': nan,
    'DEALER_TEL': nan,
    'DEALER_CITY': nan,
    'DEALER_STATE': nan,
    'DEALER_ZIP': nan,
    'PROD_TYPE': 'V',
    'REPAIRED_YN': nan,
    'MEDICAL_ATTN': 'N',
    'VEHICLES_TOWED_YN': 'N',
    'NEW_OLD': 'New',
    'FUNCTION': 'F8',
    'COMPONET': 'DOOR LATCH',
    'FAILURE': 'FROZEN',
    'BINNING': 'DOOR LATCH | FROZEN',
    'FULL_STATE': 'Illinois',
    'FAIL_QUARTER': '2022Q4',
    'EXTRACTED_DATE': '2024-01-29'
```
----

### Recalls:
```python
{
    'REPORT_RECEIVED_DATE':'10/06/1966'
    'NHTSA_ID':'66V004002'
    'RECALL_LINK':'Go to Recall (https://www.nhtsa.gov/recalls?nhtsaId=66V004002)'
    'MANUFACTURER':'Ford Motor Company'
    'SUBJECT':'INTERIOR SYSTEMS:RESTRAINT:BELT ANCHOR AND ATTACHM'
    'COMPONENT':'SEAT BELTS'
    'MFR_CAMPAIGN_NUMBER':'NR (Not Reported)'
    'RECALL_TYPE':'Vehicle'
    'POTENTIALLY_AFFECTED':'65000'
    'RECALL_DESCRIPTION':''
    'CONSEQUENCE_SUMMARY':''
    'CORRECTIVE_ACTION':''
    'PARK_OUTSIDE_ADVISORY':'No'
    'DO_NOT_DRIVE_ADVISORY':'No'
    'COMPLETION_RATE':''
}
```

### FINAL COMPLAINT:
```sql
    CMPLID CHAR(9) PRIMARY KEY
    ODINO CHAR(9)
    MFR_NAME CHAR(25)
    MAKETXT CHAR(25)
    MODELTXT CHAR(256)
    YEARTXT CHAR(4)
    CRASH BOOLEAN 
    FAILDATE CHAR(8)
    FIRE BOOLEAN 
    INJURED NUMBER(2)
    DEATHS NUMBER(2)
    COMPDESC CHAR(128)
    CITY CHAR(30)
    STATE_ CHAR(2)
    VIN CHAR(11)
    DATEA CHAR(8)
    LDATE CHAR(8)
    MILES NUMBER(7)
    OCCURENCES NUMBER(4)
    CDESCR TEXT
    CMPL_TYPE CHAR(4)
    POLICE_RPT_YN BOOLEAN
    PURCH_DT CHAR(8)
    ORIG_OWER_YN BOOLEAN
    ANTI_BRAKES_YN BOOLEAN
    CRUISE_CONT_YN BOOLEAN
    NUM_CYLS NUMBER(2)
    DRIVE_TRAIN CHAR(4)
    FUEL_SYS CHAR(4)
    FUEL_TYPE CHAR(4)
    TRASN_TYPE CHAR(4)
    VEH_SPEED NUMBER(3)
    DOT CHAR(20)
    TIRE_SIZE CHAR(30)
    LOC_OF_TIRE CHAR(4)
    TIRE_FAIL_TYPE CHAR(4)
    ORIG_EQUIP_YN BOOLEAN 
    MANUF_DT CHAR(8)
    SEAT_TYPE CHAR(4)
    RESTRAINT_TYPE CHAR(4)
    DEALER_NAME CHAR(40)
    DEALER_TEL CHAR(20)
    DEALER_CITY CHAR(30)
    DEALER_STATE CHAR(2)
    DEALER_ZIP CHAR(10)
    PROD_TYPE CHAR(4)
    REPAIRED_YN BOOLEAN
    MEDICAL_ATTN BOOLEAN
    VEHICLES_TOWED_YN BOOLEAN
    FUNCTION_ CHAR(3)
    COMPONET CHAR(20)
    FAILURE CHAR(40)
    BINNING CHAR(63)
    FULL_STATE CHAR(30)
    FAIL_QUARTER CHAR(6)
    Full_VIN CHAR(17)
    Production_Date DATE
    VFG CHAR(3)
    10_Char_MY CHAR(1)
    11_Char_Plant CHAR(1)
    8_Char_Engine CHAR(1)
    Vehicle_Line_WERS CHAR(128)
    Vehicle_Line_GSAR CHAR(128)
    Vehicle_Line_Global CHAR(128)
    Assembly_Plant CHAR(40)
    Warranty_Start_Date DATE
    Repair_Date_1 DATE
    Repair_Date_2 DATE
    EXTRACTED_DATE DATE
```

### FINAL RECALL:
```sql
    NHTSA_ID TEXT PRIMARY KEY
    REPORT_RECEIVED_DATE TEXT
    RECALL_LINK TEXT
    MANUFACTURER TEXT
    SUBJECT TEXT
    COMPONENT TEXT
    MFR_CAMPAIGN_NUMBER TEXT
    RECALL_TYPE TEXT
    POTENTIALLY_AFFECTED INTEGER
    RECALL_DESCRIPTION TEXT
    CONSEQUENCE_SUMMARY TEXT
    CORRECTIVE_ACTION TEXT
    PARK_OUTSIDE_ADVISORY TEXT
    DO_NOT_DRIVE_ADVISORY TEXT
    COMPLETION_RATE REAL
    FUNCTION: TEXT
    FAILURE_MODE: TEXT
    EXTRACTED_DATE: DATE
```
