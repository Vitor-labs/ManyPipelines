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
    'VEHICLES_TOWED_YN': 'N'
```

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
----

### DATA COMPLAINT:
```sql
    CMPLID INTEGER PRIMARY KEY
    ODINO INTEGER                --X
    MFR_NAME TEXT
    MAKETXT TEXT                 --X
    MODELTXT TEXT                --X
    YEARTXT TEXT                 --X
    CRASH INTEGER 
    FAILDATE TEXT                --X
    FIRE INTEGER 
    INJURED INTEGER
    DEATHS INTEGER
    COMPDESC TEXT
    CITY TEXT
    STATE_ TEXT                  --X
    VIN TEXT                     --X
    DATEA TEXT                   --X
    LDATE TEXT
    MILES INTEGER                --X
    OCCURENCES INTEGER
    CDESCR TEXT                  --X
    CMPL_TYPE TEXT
    POLICE_RPT_YN INTEGER
    PURCH_DT TEXT
    ORIG_OWER_YN INTEGER
    ANTI_BRAKES_YN INTEGER
    CRUISE_CONT_YN INTEGER
    NUM_CYLS INTEGER
    DRIVE_TRAIN CHAR
    FUEL_SYS TEXT
    FUEL_TYPE TEXT
    TRASN_TYPE TEXT
    VEH_SPEED INTEGER
    DOT TEXT
    TIRE_SIZE TEXT
    LOC_OF_TIRE TEXT
    TIRE_FAIL_TYPE TEXT
    ORIG_EQUIP_YN INTEGER 
    MANUF_DT TEXT
    SEAT_TYPE TEXT
    RESTRAINT_TYPE TEXT
    DEALER_NAME TEXT
    DEALER_TEL TEXT
    DEALER_CITY TEXT
    DEALER_STATE TEXT
    DEALER_ZIP TEXT
    PROD_TYPE TEXT
    REPAIRED_YN INTEGER
    MEDICAL_ATTN INTEGER
    VEHICLES_TOWED_YN INTEGER
    FUNCTION_ TEXT               --X
    COMPONET TEXT
    FAILURE TEXT
    BINNING TEXT                 --X
    FULL_STATE TEXT
    FAIL_QUARTER TEXT            --X
    FULL_VIN TEXT                --X
    PROD_DATE DATE               --X
    VFG TEXT                     --X
    VEHICLE_LINE_WERS TEXT       --X
    VEHICLE_LINE_GSAR TEXT       --X
    VEHICLE_LINE_Global TEXT     --X
    ASSEMBLY_PLANT TEXT          --X
    WARRANTY_START_DATE DATE
    EXTRACTED_DATE DATE          --X
    FAILURE_MODE TEXT            --X
    MILEAGE_CLASS TEXT           --X
```

### DATA RECALL:
```sql
    NHTSA_ID TEXT PRIMARY KEY    --X
    REPORT_RECEIVED_DATE TEXT    --X
    RECALL_LINK TEXT             --X
    MANUFACTURER TEXT            --X
    SUBJECT_ TEXT
    COMPONENT TEXT               --X
    MFR_CAMPAIGN_NUMBER TEXT
    RECALL_TYPE TEXT             --X
    POTENTIALLY_AFFECTED INTEGER --X
    RECALL_DESCRIPTION TEXT      --X
    CONSEQUENCE_SUMMARY TEXT     --X
    CORRECTIVE_ACTION TEXT
    PARK_OUTSIDE_ADVISORY TEXT
    DO_NOT_DRIVE_ADVISORY TEXT
    COMPLETION_RATE REAL
    FUNCTION_: TEXT              --X
    FAILURE_MODE: TEXT           --X
    EXTRACTED_DATE: DATE         --X
```

### GRID DATA:
```sql
    MODEL TEXT
    BINING TEXT
    ISSUE TEXT
    FUNCTION_ TEXT
    ISSUE_TITLE TEXT 
    DESCRIPTION_ TEXT 
    AFFECTED_VEHICLES TEXT 
    DAYS_OPEN_IN_CCRG INTEGER
    DAYS_OPEN_IN_CSF INTEGER
    DAYS_OPEN_IN_GOV INTEGER
    DAYS_OPEN_IN_EPRC INTEGER
    FCA TEXT
    OVERALL_STATUS TEXT
    GRID_CREATION_DATE TEXT
```
