import xml.etree.ElementTree as ET
from typing import List
from openpyxl.worksheet.worksheet import Worksheet
from .utils import strip_namespace, safe_text

SHEET_NAME = "ResUnitAmenities"

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


def export_resunitamenities(xml_path: str, ws: Worksheet) -> None:
    """
    Writes one sheet:
      DataSection/ResUnitAmenities/ResUnitAmenity -> rows
    """
    ws.title = SHEET_NAME
    ws.append(RES_UNIT_AMENITIES_COLUMNS)

    # Track parents so we can clear fully and safely
    context = ET.iterparse(xml_path, events=("start", "end"))
    parents = []

    for event, elem in context:
        if event == "start":
            parents.append(elem)
            continue

        # event == "end"
        if strip_namespace(elem.tag) == "ResUnitAmenity":
            row_map = {c: "" for c in RES_UNIT_AMENITIES_COLUMNS}

            for child in elem:
                key = strip_namespace(child.tag)
                if key in row_map:
                    row_map[key] = safe_text(child.text)

            ws.append([row_map[c] for c in RES_UNIT_AMENITIES_COLUMNS])

            # Clear this element to free memory
            elem.clear()

            # Also clear already-processed siblings from its parent (important for streaming)
            if len(parents) >= 2:
                parent = parents[-2]
                while len(parent) > 0 and parent[0] is not elem:
                    del parent[0]

        # pop current elem from stack
        parents.pop()
