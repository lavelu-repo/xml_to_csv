import xml.etree.ElementTree as ET
from typing import Callable, Dict, List, Optional
from openpyxl.worksheet.worksheet import Worksheet
import logging

logger = logging.getLogger(__name__)


def strip_namespace(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def safe_text(text: Optional[str]) -> str:
    return "" if text is None else str(text).strip()


def export_table_to_sheet(
    xml_path: str,
    ws: Worksheet,
    *,
    sheet_name: str,
    row_tag: str,
    columns: List[str],
    root_path: Optional[List[str]] = None,
    strip_ns: Callable[[str], str] = strip_namespace,
    safe_txt: Callable[[Optional[str]], str] = safe_text,
) -> None:
    """
    Generic streaming XML -> Excel exporter.

    - sheet_name: Excel sheet name
    - row_tag: element name representing ONE row (e.g. "ResUnitAmenity")
    - columns: ordered list of column names to output
    - root_path: optional container path to enforce context (e.g. ["DataSection","ResUnitAmenities"])
    """
    logger.info("Exporting sheet %s (row_tag=%s)", sheet_name, row_tag)
    ws.title = sheet_name
    ws.append(columns)

    context = ET.iterparse(xml_path, events=("start", "end"))
    stack: List[str] = []
    parents: List[ET.Element] = []
    rows_written = 0

    def in_root_path() -> bool:
        if not root_path:
            return True
        rp = root_path
        if len(stack) < len(rp):
            return False
        # contiguous match anywhere in the stack
        for i in range(0, len(stack) - len(rp) + 1):
            if stack[i : i + len(rp)] == rp:
                return True
        return False

    for event, elem in context:
        if event == "start":
            stack.append(strip_ns(elem.tag))
            parents.append(elem)
            continue

        tag = strip_ns(elem.tag)
        if tag == row_tag and in_root_path():
            row_map: Dict[str, str] = {c: "" for c in columns}

            for child in elem:
                key = strip_ns(child.tag)
                if key in row_map:
                    row_map[key] = safe_txt(child.text)

            ws.append([row_map[c] for c in columns])
            rows_written += 1
            if logger.isEnabledFor(10):
                # DEBUG level (10) shows row detail
                logger.debug("Appended row to %s: %s", ws.title, {k: v for k, v in row_map.items() if v})

            # memory-friendly clearing
            elem.clear()
            if len(parents) >= 2:
                parent = parents[-2]
                # delete processed siblings
                while len(parent) > 0 and parent[0] is not elem:
                    del parent[0]

        stack.pop()
        parents.pop()

    logger.info("Wrote %d rows to sheet %s", rows_written, sheet_name)
