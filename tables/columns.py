from typing import List, Dict, TypedDict, Optional


class TableSpec(TypedDict):
    sheet_name: str
    row_tag: str
    columns: List[str]
    root_path: Optional[List[str]]


# Constants for each table's sheet name and columns. These are used by the generic export function in export.py.
# ---- CommProperties ----
COMM_PROPERTIES_SHEET_NAME = "CommProperties"
COMM_PROPERTIES_COLUMNS: List[str] = [
    "Record_ID",
    "Source_Id",
    "Source_Code",
    "Address1",
    "Address2",
    "Address3",
    "Address4",
    "City",
    "State",
    "ZipCode",
    "Residential",
    "Commercial",
    "Association",
    "Student",
    "Senior",
    "Military",
    "Affordable",
    "PublicHousing",
    "International",
    "CanadianSocialHousing",
    "AssocSubType",
    "EndOfYear",
    "Inactive",
    "InactiveDate",
    "PurchasePrice",
    "NCREIFNumber",
    "AcquisitionDate",
    "DispositionDate",
    "LateType",
    "LatePercent",
    "LatePerDay",
    "LateMin",
    "Type2",
    "IsEstate",
    "ContractExpDate",
    "ContractReserve",
    "Commision",
    "MinCommision",
]

# ---- LockOuts ----
LOCK_OUTS_SHEET_NAME = "LockOuts"
LOCK_OUTS_COLUMNS: List[str] = [
    "Record_ID",
    "Source_ID",
    "PropertyID",
    "DTMMYY0",
    "DTMMYY1",
    "DTMMYY2",
    "DTMMYY3",
    "DTMMYY4",
    "DTMMYY5",
    "ICLOSEDAY",
    "HCHART",
    "DTCHARGEPOST",
    "IFUNDTYPE",
    "PERFORMANCE",
    "dtLeaseWeek",
    "dtCurrentCAMYear",
    "dtDailyClose",
]

# ---- ResSourceNames ----
RES_SOURCE_NAMES_SHEET_NAME = "ResSourceNames"
RES_SOURCE_NAMES_COLUMNS: List[str] = [
    "Record_ID",
    "Source_ID",
    "PropertyId",
    "SourceName",
    "InactiveDate",
    "Portal",
]

# ---- ResAgentNames ----
RES_AGENT_NAMES_SHEET_NAME = "ResAgentNames"
RES_AGENT_NAMES_COLUMNS: List[str] = [
    "Record_ID",
    "Source_ID",
    "Source_Code",
    "PropertyId",
    "AgentName",
    "DateEnd",
    "EmployeeID",
    "StartDate",
]

# ---- ResCancelReasons ----
RES_CANCEL_REASONS_SHEET_NAME = "ResCancelReasons"
RES_CANCEL_REASONS_COLUMNS: List[str] = [
    "Record_ID",
    "Source_ID",
    "PropertyId",
    "Reason",
    "InactiveDate",
    "ContactResult",
    "UnqualifiedTraffic",
    "CancelApplication",
    "Deny",
    "CancelMoveIn",
    "ApproveApplication",
]

# ---- ResRentableItemsTypes ----
RES_RENTABLE_ITEMS_TYPES_SHEET_NAME = "ResRentableItemsTypes"
RES_RENTABLE_ITEMS_TYPES_COLUMNS: List[str] = [
    "Record_ID",
    "Source_ID",
    "Source_Code",
    "PropertyId",
    "ChargeCodeId",
    "Description",
    "Rent",
    "Deposit",
    "Tax",
    "ServiceCharge",
]

# ---- ResUnitAmenities ----
RES_UNIT_AMENITIES_SHEET_NAME = "ResUnitAmenities"
RES_UNIT_AMENITIES_COLUMNS: List[str] = [
    "Record_ID",
    "Source_ID",
    "Source_Code",
    "UnitId",
    "Name",
    "Amenity",
    "Prior",
    "PriorDate",
    "Current",
    "CurrentDate",
    "Proposed",
    "ProposedDate",
    "Notes",
]

# Add more table constants here in the same style...


# One place to register all tables you want to export
TABLE_SPECS: Dict[str, TableSpec] = {
    "comm_properties": {
        "sheet_name": COMM_PROPERTIES_SHEET_NAME,
        "row_tag": "CommProperty",
        "columns": COMM_PROPERTIES_COLUMNS,
        "root_path": ["DataSection", "CommProperties"],
    },
    "lock_outs": {
        "sheet_name": LOCK_OUTS_SHEET_NAME,
        "row_tag": "LockOut",
        "columns": LOCK_OUTS_COLUMNS,
        "root_path": ["DataSection", "LockOuts"],
    },
    "res_unit_amenities": {
        "sheet_name": RES_UNIT_AMENITIES_SHEET_NAME,
        "row_tag": "ResUnitAmenity",
        "columns": RES_UNIT_AMENITIES_COLUMNS,
        "root_path": ["DataSection", "ResUnitAmenities"],
    },
}
