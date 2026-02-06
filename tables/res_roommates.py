import xml.etree.ElementTree as ET
from typing import List
from openpyxl.worksheet.worksheet import Worksheet
from .utils import strip_namespace, safe_text

SHEET_NAME = "ResRoommates"

RES_ROOMMATES_COLUMNS: List[str] = [
    "IsOccupant",
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
