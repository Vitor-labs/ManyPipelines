schema_type: dataframe
version: 0.18.0
columns:
  CMPLID:
    title: null
    description: null
    dtype: int64
    nullable: false
    checks:
      greater_than_or_equal_to: 1633291.0
      less_than_or_equal_to: 1966894.0
    unique: false
    coerce: false
    required: true
    regex: false
  ODINO:
    title: null
    description: null
    dtype: int64
    nullable: false
    checks:
      greater_than_or_equal_to: 565713.0
      less_than_or_equal_to: 11572265.0
    unique: false
    coerce: false
    required: true
    regex: false
  MFR_NAME:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  MAKETXT:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  MODELTXT:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  YEARTXT:
    title: null
    description: null
    dtype: float64
    nullable: true
    checks:
      greater_than_or_equal_to: 1960.0
      less_than_or_equal_to: 9999.0
    unique: false
    coerce: false
    required: true
    regex: false
  CRASH:
    title: null
    description: null
    dtype: object
    nullable: false
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  FAILDATE:
    title: null
    description: null
    dtype: int64
    nullable: false
    checks:
      greater_than_or_equal_to: 19170101.0
      less_than_or_equal_to: 20240215.0
    unique: false
    coerce: false
    required: true
    regex: false
  FIRE:
    title: null
    description: null
    dtype: object
    nullable: false
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  INJURED:
    title: null
    description: null
    dtype: int64
    nullable: false
    checks:
      greater_than_or_equal_to: 0.0
      less_than_or_equal_to: 99.0
    unique: false
    coerce: false
    required: true
    regex: false
  DEATHS:
    title: null
    description: null
    dtype: int64
    nullable: false
    checks:
      greater_than_or_equal_to: 0.0
      less_than_or_equal_to: 99.0
    unique: false
    coerce: false
    required: true
    regex: false
  COMPDESC:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  CITY:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  STATE:
    title: null
    description: null
    dtype: object
    nullable: false
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  VIN:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  DATEA:
    title: null
    description: null
    dtype: int64
    nullable: false
    checks:
      greater_than_or_equal_to: 20200101.0
      less_than_or_equal_to: 20240215.0
    unique: false
    coerce: false
    required: true
    regex: false
  LDATE:
    title: null
    description: null
    dtype: int64
    nullable: false
    checks:
      greater_than_or_equal_to: 20200101.0
      less_than_or_equal_to: 20240215.0
    unique: false
    coerce: false
    required: true
    regex: false
  MILES:
    title: null
    description: null
    dtype: float64
    nullable: true
    checks:
      greater_than_or_equal_to: 0.0
      less_than_or_equal_to: 9848609.0
    unique: false
    coerce: false
    required: true
    regex: false
  OCCURENCES:
    title: null
    description: null
    dtype: float64
    nullable: true
    checks:
      greater_than_or_equal_to: 0.0
      less_than_or_equal_to: 40.0
    unique: false
    coerce: false
    required: true
    regex: false
  CDESCR:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  CMPL_TYPE:
    title: null
    description: null
    dtype: object
    nullable: false
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  POLICE_RPT_YN:
    title: null
    description: null
    dtype: object
    nullable: false
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  PURCH_DT:
    title: null
    description: null
    dtype: float64
    nullable: true
    checks:
      greater_than_or_equal_to: 19840613.0
      less_than_or_equal_to: 20240101.0
    unique: false
    coerce: false
    required: true
    regex: false
  ORIG_OWER_YN:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  ANTI_BRAKES_YN:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  CRUISE_CONT_YN:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  NUM_CYLS:
    title: null
    description: null
    dtype: float64
    nullable: true
    checks:
      greater_than_or_equal_to: 0.0
      less_than_or_equal_to: 16.0
    unique: false
    coerce: false
    required: true
    regex: false
  DRIVE_TRAIN:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  FUEL_SYS:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  FUEL_TYPE:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  TRASN_TYPE:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  VEH_SPEED:
    title: null
    description: null
    dtype: float64
    nullable: true
    checks:
      greater_than_or_equal_to: 0.0
      less_than_or_equal_to: 999.0
    unique: false
    coerce: false
    required: true
    regex: false
  DOT:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  TIRE_SIZE:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  LOC_OF_TIRE:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  TIRE_FAIL_TYPE:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  ORIG_EQUIP_YN:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  MANUF_DT:
    title: null
    description: null
    dtype: float64
    nullable: true
    checks:
      greater_than_or_equal_to: 20020501.0
      less_than_or_equal_to: 20231021.0
    unique: false
    coerce: false
    required: true
    regex: false
  SEAT_TYPE:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  RESTRAINT_TYPE:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  DEALER_NAME:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  DEALER_TEL:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  DEALER_CITY:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  DEALER_STATE:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  DEALER_ZIP:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  PROD_TYPE:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  REPAIRED_YN:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  MEDICAL_ATTN:
    title: null
    description: null
    dtype: object
    nullable: false
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
  VEHICLES_TOWED_YN:
    title: null
    description: null
    dtype: object
    nullable: true
    checks: null
    unique: false
    coerce: false
    required: true
    regex: false
checks: null
index:
- title: null
  description: null
  dtype: int64
  nullable: false
  checks:
    greater_than_or_equal_to: 0.0
    less_than_or_equal_to: 333525.0
  name: null
  unique: false
  coerce: false
dtype: null
coerce: true
strict: false
name: null
ordered: false
unique: null
report_duplicates: all
unique_column_names: false
add_missing_columns: false
title: null
description: null
