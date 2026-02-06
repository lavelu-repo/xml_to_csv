import xml.etree.ElementTree as ET
from typing import List
from openpyxl.worksheet.worksheet import Worksheet
from .utils import strip_namespace, safe_text

SHEET_NAME = "CommUnits"

COMM_UNITS_COLUMNS: List[str] = [
    "Record_ID",
    "Source_Id",
    "Source_Code",
    "PropertyId",
    "Exclude",
    "UnitTypeId",
    "Rent",
    "Sqft",
    "IsRentReady",
    "BuildingId",
    "FloorId",
    "HoldUntil",
    "DateReady",
    "RentalType",
    "RentObject",
    "TotalRooms",
    "Status",
    "BedroomCount",
    "AffContractRent",
    "AffSetAside",
    "AffUtilityAllowance",
    "AffContractNo",
    "AffAlternateId",
    "IsPortalExcluded",
    "PortalDisplayRank",
    "DateAvailable",
    "DateVacant",
    "DEPOSIT0",
    "DEPOSIT1",
    "DEPOSIT2",
    "DEPOSIT3",
    "DEPOSIT4",
    "DEPOSIT5",
    "DEPOSIT6",
    "DEPOSIT7",
    "DEPOSIT8",
    "DEPOSIT9",
    "PASTRENT0",
    "PASTRENT1",
    "PASTRENT2",
    "PASTRENT3",
    "PASTRENT4",
    "PASTRENT5",
    "PASTRENT6",
    "PASTRENT7",
    "PASTRENT8",
    "PASTRENT9",
    "PASTRENT10",
    "PASTRENT11",
    "DatePASTRENTINC0",
    "DatePASTRENTINC1",
    "DatePASTRENTINC2",
    "DatePASTRENTINC3",
    "DatePASTRENTINC4",
    "DatePASTRENTINC5",
    "DatePASTRENTINC6",
    "DatePASTRENTINC7",
    "DatePASTRENTINC8",
    "DatePASTRENTINC9",
    "DatePASTRENTINC10",
    "DatePASTRENTINC11",
    "Performance",
]


def export_communits(xml_path: str, ws: Worksheet) -> None:
    """
    Writes one sheet:
      DataSection/CommUnits/CommUnit -> rows
    """
    ws.title = SHEET_NAME
    ws.append(COMM_UNITS_COLUMNS)

    # Stream parse; write a row when </CommUnit> closes
    for event, elem in ET.iterparse(xml_path, events=("end",)):
        if strip_namespace(elem.tag) == "CommUnit":
            row_map = {c: "" for c in COMM_UNITS_COLUMNS}

            for child in elem:
                key = strip_namespace(child.tag)
                if key in row_map:
                    row_map[key] = safe_text(child.text)

            ws.append([row_map[c] for c in COMM_UNITS_COLUMNS])
            elem.clear()
