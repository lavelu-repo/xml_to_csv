import xml.etree.ElementTree as ET
from typing import List
from openpyxl.worksheet.worksheet import Worksheet
from .utils import strip_namespace, safe_text

SHEET_NAME = "CommProperties"

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

def export_commproperties(xml_path: str, ws: Worksheet) -> None:
    """
    Writes one sheet:
      DataSection/CommProperties/CommProperty -> rows
    """
    ws.title = SHEET_NAME
    ws.append(COMM_PROPERTIES_COLUMNS)

    # Stream parse; write a row when </CommProperty> closes
    for event, elem in ET.iterparse(xml_path, events=("end",)):
        if strip_namespace(elem.tag) == "CommProperty":
            row_map = {c: "" for c in COMM_PROPERTIES_COLUMNS}

            for child in elem:
                key = strip_namespace(child.tag)
                if key in row_map:
                    row_map[key] = safe_text(child.text)

            ws.append([row_map[c] for c in COMM_PROPERTIES_COLUMNS])
            elem.clear()
