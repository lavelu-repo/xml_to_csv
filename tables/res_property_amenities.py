import xml.etree.ElementTree as ET
from typing import List
from openpyxl.worksheet.worksheet import Worksheet
from .utils import strip_namespace, safe_text

SHEET_NAME = "ResPropertyAmenities"

RES_PROPERTY_AMENITIES_COLUMNS: List[str] = [
    "Record_ID",
    "Source_ID",
    "Source_Code",
    "PropertyId",
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


def export_respropertyamenities(xml_path: str, ws: Worksheet) -> None:
    """
    Writes one sheet:
      DataSection/ResPropertyAmenities/ResPropertyAmenity -> rows
    """
    ws.title = SHEET_NAME
    ws.append(RES_PROPERTY_AMENITIES_COLUMNS)

    # Stream parse; write a row when </ResPropertyAmenity> closes
    for event, elem in ET.iterparse(xml_path, events=("end",)):
        if strip_namespace(elem.tag) == "ResPropertyAmenity":
            row_map = {c: "" for c in RES_PROPERTY_AMENITIES_COLUMNS}

            for child in elem:
                key = strip_namespace(child.tag)
                if key in row_map:
                    row_map[key] = safe_text(child.text)

            ws.append([row_map[c] for c in RES_PROPERTY_AMENITIES_COLUMNS])
            elem.clear()
