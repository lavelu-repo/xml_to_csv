import xml.etree.ElementTree as ET
from typing import List
from openpyxl.worksheet.worksheet import Worksheet
from .utils import strip_namespace, safe_text

SHEET_NAME = "ResRoommates"

RES_ROOMMATES_COLUMNS: List[str] = [
    "Record_ID",
    "Source_Id",
    "Source_Code",
    "TenantId",
    "LastName",
    "FirstName",
    "MiddleName",
    "Salutation",
    "Email",
    "GovernmentId",
    "MoveIn",
    "MoveOut",
    "IsOccupant",
    "AchOptOut",
    "Relationship",
    "Notes",
    "Address1",
    "Address2",
    "Address3",
    "Address4",
    "City",
    "State",
    "ZipCode",
    "sField1",
    "sField2",
    "sField3",
    "sField4",
    "sField5",
    "sField6",
    "sField7",
    "sField8",
    "sField9",
    "sField10",
    "SPhone1",
    "SPhone2",
    "SPhone3",
    "SPhone4",
    "OccupantType",
    "AltEmail",
]


def export_resproommates(xml_path: str, ws: Worksheet) -> None:
    """
    Writes one sheet:
      DataSection/ResRoommates/ResRoommate -> rows
    """
    ws.title = SHEET_NAME
    ws.append(RES_ROOMMATES_COLUMNS)

    # Stream parse; write a row when </ResRoommate> closes
    for event, elem in ET.iterparse(xml_path, events=("end",)):
        if strip_namespace(elem.tag) == "ResRoommate":
            row_map = {c: "" for c in RES_ROOMMATES_COLUMNS}

            for child in elem:
                key = strip_namespace(child.tag)
                if key in row_map:
                    row_map[key] = safe_text(child.text)

            ws.append([row_map[c] for c in RES_ROOMMATES_COLUMNS])
            elem.clear()
