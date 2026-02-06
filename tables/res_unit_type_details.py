import xml.etree.ElementTree as ET
from typing import List
from openpyxl.worksheet.worksheet import Worksheet
from .utils import strip_namespace, safe_text

SHEET_NAME = "ResUnitTypeDetails"

RES_UNIT_TYPE_DETAILS_COLUMNS: List[str] = [
    "UnitTypeId",
    "Amount",
    "IsTaxable",
    "IsRecur",
    "MoveIn",
    "Remarks",
    "Acct",
    "IsRequired",
    "IsModified",
    "Instances",
    "Duration",
    "StartMonthsNum",
    "RentObject",
    "IsRoommate",
    "IsSpouse",
    "IsGuarantor",
    "IsOther",
]


def export_resunittypedetails(xml_path: str, ws: Worksheet) -> None:
    """
    Writes one sheet:
      DataSection/ResUnitTypeDetails/ResUnitTypeDetail -> rows
    """
    ws.title = SHEET_NAME
    ws.append(RES_UNIT_TYPE_DETAILS_COLUMNS)

    # Stream parse; write a row when </ResUnitTypeDetail> closes
    for event, elem in ET.iterparse(xml_path, events=("end",)):
        if strip_namespace(elem.tag) == "ResUnitTypeDetail":
            row_map = {c: "" for c in RES_UNIT_TYPE_DETAILS_COLUMNS}

            for child in elem:
                key = strip_namespace(child.tag)
                if key in row_map:
                    row_map[key] = safe_text(child.text)

            ws.append([row_map[c] for c in RES_UNIT_TYPE_DETAILS_COLUMNS])
            elem.clear()
