import xml.etree.ElementTree as ET
from typing import List
from openpyxl.worksheet.worksheet import Worksheet
from .utils import strip_namespace, safe_text

SHEET_NAME = "ResUnitTypes"

RES_UNIT_TYPES_COLUMNS: List[str] = [
    "Record_ID",
    "Source_Id",
    "Source_Code",
    "Description",
    "Rent",
    "Deposit",
    "Sqft",
    "PropertyId",
    "Beds",
    "Baths",
    "MinRent",
    "MaxRent",
]


def export_resunittypes(xml_path: str, ws: Worksheet) -> None:
    """
    Writes one sheet:
      DataSection/ResUnitTypes/ResUnitType -> rows
    """
    ws.title = SHEET_NAME
    ws.append(RES_UNIT_TYPES_COLUMNS)

    # Stream parse; write a row when </ResUnitType> closes
    for event, elem in ET.iterparse(xml_path, events=("end",)):
        if strip_namespace(elem.tag) == "ResUnitType":
            row_map = {c: "" for c in RES_UNIT_TYPES_COLUMNS}

            for child in elem:
                key = strip_namespace(child.tag)
                if key in row_map:
                    row_map[key] = safe_text(child.text)

            ws.append([row_map[c] for c in RES_UNIT_TYPES_COLUMNS])
            elem.clear()
