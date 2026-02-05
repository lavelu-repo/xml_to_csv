import xml.etree.ElementTree as ET
from typing import List
from openpyxl.worksheet.worksheet import Worksheet
from .utils import strip_namespace, safe_text

SHEET_NAME = "LockOuts"

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


def export_lockouts(xml_path: str, ws: Worksheet) -> None:
    """
    Writes one sheet:
      DataSection/LockOuts/LockOut -> rows
    """
    ws.title = SHEET_NAME
    ws.append(LOCK_OUTS_COLUMNS)

    # Stream parse; write a row when </LockOut> closes
    for event, elem in ET.iterparse(xml_path, events=("end",)):
        if strip_namespace(elem.tag) == "LockOut":
            row_map = {c: "" for c in LOCK_OUTS_COLUMNS}

            for child in elem:
                key = strip_namespace(child.tag)
                if key in row_map:
                    row_map[key] = safe_text(child.text)

            ws.append([row_map[c] for c in LOCK_OUTS_COLUMNS])
            elem.clear()
