CREATE TABLE IF NOT EXISTS Dim_Location (
  LOCATION_ID TEXT PRIMARY KEY, -- LIKE: SUFFIX AGGREGATION 'NA-USA-SW-AL'
  MARKET TEXT NOT NULL, 				-- LIKE: NORTH AMERICA, EUROPEAN UNION, SOUTH AMERICA, GREATER CHINA
  MARKET_SUFFIX TEXT NOT NULL,	-- LIKE: NA, EU, SA, GC
  COUNTRY TEXT NOT NULL,				-- LIKE: UNITED STATES, BRAZIL, FRANCE, CHINA
  COUNTRY_SUFFIX TEXT NOT NULL,	-- LIKE: USA, BR, FR, CH
  REGION TEXT NOT NULL,					-- LIKE: SOUTHWEST, NORTHEAST
  SUB_REGION TEXT NOT NULL,			-- LIKE: EAST SOUTH CENTRAL
  STATE_ TEXT NOT NULL,					-- LIKE: Alabama, North Carolina
  STATE_SUFFIX TEXT NOT NULL		-- LIKE: AL, NC
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS Dim_VinInfo (
	VIN TEXT PRIMARY KEY,			-- 17 Length String
	VEHICLE_LINE_WERS TEXT,
	VEHICLE_LINE_GSAR TEXT,
	VEHICLE_LINE_Global TEXT,
	ASSEMBLY_PLANT TEXT,
	FUEL_TYPE TEXT,
	FUEL_TYPE_ENG TEXT,
	PROD_DATE TEXT CHECK(length(PROD_DATE) == 10),
	WARRANTY_START_DATE TEXT CHECK(length(WARRANTY_START_DATE) == 10),
	MODIFIED_AT TEXT CHECK(length(MODIFIED_AT) == 10)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS Dim_Problems (
	BINNING TEXT PRIMARY KEY, 			-- "PROBLEMATIC_PART | FAILURE_CASE" string
	FUNCTION_ TEXT NOT NULL,				-- For now we only work with F8 and F3 cases.
	VFG TEXT NOT NULL,							-- Binning Group, aggregated by comoponent
	PROBLEMATIC_PART TEXT NOT NULL,	-- Component that got the Complaint
	FAILURE_CASE TEXT NOT NULL,			-- Motivation of the Complaint
	FAILURE_MODE TEXT NOT NULL			-- Group of commom Failure Cases
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS Dim_Recalls (
	NHTSA_ID TEXT PRIMARY KEY,
	REPORT_RECEIVED_DATE TEXT NOT NULL CHECK(length(REPORT_RECEIVED_DATE) == 10),
	RECALL_LINK TEXT NOT NULL,
	MANUFACTURER TEXT NOT NULL,
	SUBJECT_ TEXT NOT NULL,
	COMPONENT TEXT NOT NULL,
	MFR_CAMPAIGN_NUMBER TEXT,
	RECALL_TYPE TEXT,
	POTENTIALLY_AFFECTED INTEGER,
	RECALL_DESCRIPTION TEXT,
	CONSEQUENCE_SUMMARY TEXT,
	CORRECTIVE_ACTION TEXT,
	IS_OPEN INTEGER NOT NULL,     			-- Boolean Field, 0: No, 1: Yes
	EXTRACTED_DATE DATE CHECK(length(EXTRACTED_DATE) == 10),

	-- Foreign keys definitions
	PROBLEM_ID TEXT NOT NULL,
	FOREIGN KEY (PROBLEM_ID) REFERENCES Dim_Problems (BINNING) ON UPDATE CASCADE ON DELETE SET NULL
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS Dim_Grid (
	ISSUE TEXT PRIMARY KEY,
	MODEL TEXT NOT NULL,
	ISSUE_TITLE TEXT NOT NULL,
	DESCRIPTION_ TEXT  NOT NULL,
	AFFECTED_VEHICLES TEXT  NOT NULL,
	DAYS_OPEN_IN_CCRG INTEGER,
	DAYS_OPEN_IN_CSF INTEGER,
	DAYS_OPEN_IN_GOV INTEGER,
	DAYS_OPEN_IN_EPRC INTEGER,
	FCA TEXT NOT NULL,
	OVERALL_STATUS TEXT NOT NULL,
	GRID_CREATION_DATE TEXT NOT NULL CHECK(length(GRID_CREATION_DATE) == 10),

	-- Foreign keys definitions
	PROBLEM_ID TEXT NOT NULL,
	FOREIGN KEY (PROBLEM_ID) REFERENCES Dim_Problems (BINNING) ON UPDATE CASCADE ON DELETE SET NULL
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS Fact_Complaints (
	ODINO INTEGER PRIMARY KEY,
	MFR_NAME TEXT NOT NULL,
	MAKETXT TEXT NOT NULL,
	MODELTXT TEXT NOT NULL,
	YEARTXT TEXT NOT NULL,
	LDATE TEXT NOT NULL,
	MILES INTEGER,
	OCCURENCES INTEGER,
	CDESCR TEXT NOT NULL,
	MILEAGE_CLASS TEXT NOT NULL,
	FAILDATE TEXT NOT NULL CHECK(length(FAILDATE) == 10),
	FAIL_QUARTER TEXT NOT NULL CHECK(length(FAIL_QUARTER) == 6),
	EXTRACTED_DATE TEXT NOT NULL CHECK(length(EXTRACTED_DATE) == 10),

	-- Foreign keys definitions
	VIN TEXT UNIQUE NOT NULL,
	PROBLEM_ID TEXT,
	LOCATION_ID TEXT,
	GRID_ID INTEGER,
	RECALL_ID TEXT,

	--VERIFY RELATIONSHIPS BETWEEN TABLES
	FOREIGN KEY (VIN) REFERENCES Dim_VinInfo (VIN) ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY (PROBLEM_ID) REFERENCES Dim_Problems (BINNING) ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY (LOCATION_ID) REFERENCES Dim_Location (LOCATION_ID)	ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY (GRID_ID)	REFERENCES Dim_Grid (GRID_ID) ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY (RECALL_ID) REFERENCES Dim_Recalls (RECALL_ID) ON UPDATE CASCADE ON DELETE SET NULL
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS Fact_Warraties (
	WARRANTY_ID INTEGER UNIQUE PRIMARY KEY,
	STATUS_ TEXT,													-- Open, closed or monitoring (possiboly relates to FSA)
	CLAIM_KEY REAL,												-- ID for Repairs (LIKE ODINO)
	CLAIM_TYPE TEXT,											-- Acronims for claim (verify with lucas)
	DTC TEXT,															-- Stands for 'Diagnostic Trouble Code'
	TIS INTEGER,													-- Time in service (number of months)
	ODO INTEGER,													-- maybe stands for odometer (car miles ?)
	CLAIN_DATA TEXT CHECK(length(CLAIN_DATA) == 10),
	REPAIR_DATE TEXT CHECK(length(REPAIR_DATE) == 10),
	VEHICLE_BUILD_DATE TEXT CHECK(length(VEHICLE_BUILD_DATE) == 10),
	MODEL_YEAR INTEGER,
	VEHICLE_TYPE TEXT,
	PROPUTION_TYPE TEXT,
	CAUSAL_BASE TEXT,											-- Primary (real ?) cause of the problem ?
	MATERIAL_COST REAL,
	TOTAL_COST REAL,
	PACK_SN TEXT,													-- Giant Big Crazy Code
	ECB_BINNING TEXT,
	CREATED_AT TEXT CHECK(length(CREATED_AT) == 10),
	MODIFIED_AT TEXT CHECK(length(MODIFIED_AT) == 10),
	REPLACED_PARTS TEXT,
	TECHNICAL_COMMENTS TEXT,
	CUSTOEMER_COMMENTS TEXT,
	DEALER TEXT,
	CAUSAL_PREFIX TEXT,
	CAUSAL_SUFFIX TEXT,
	COND_CODE TEXT,												-- Code of gta 6 sheets
	NOTES TEXT,
	AWS_MAINTENANCE_DATE TEXT,	  				-- Load (Cutoff) date
	ALIAS TEXT,
	CLAIM_STATUS TEXT,
	ECB INTEGER,													-- Boolean field for something
	PACK_BUILD_DATE TEXT CHECK(length(PACK_BUILD_DATE) == 10),
	COUNT_RELATED_COMPONENT INTEGER,
	T50$ INTEGER,													-- no one knows, realy great music
	T50_ INTEGER,
	ECB_COMMENTS TEXT,										-- kill latter
	T50$_STATUS INTEGER,
	T50_STATUS INTEGER,
	CUST_IMPACT TEXT,											-- maybe is important, maintain
	MATCH_EXEMPT INTEGER,
	PRIMARY_DTCS TEXT,
	ECB_EXCEPTION INTEGER,
	ID_DEL INTEGER,
	WCC TEXT NOT NULL,										-- VFG part specificaiton
	CCC TEXT NOT NULL,										-- other minor VFG part specificaiton
	SYSTEM_EXPORT TEXT,
	CREATED_BY TEXT 
	MODIFIED_BY TEXT,
	KEYWORDS TEXT,												-- Created at processemnt

	-- Foreign keys definitions
	PROBLEM_ID TEXT,
	LOCATION_ID INTEGER,

	FOREIGN KEY (PROBLEM_ID) REFERENCES Dim_Problems (BINNING) ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY (LOCATION_ID) REFERENCES Dim_Location (LOCATION_ID) ON UPDATE CASCADE ON DELETE SET NULL
) WITHOUT ROWID;
