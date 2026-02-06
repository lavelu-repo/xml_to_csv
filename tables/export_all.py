from openpyxl import Workbook
from .columns import TABLE_SPECS
from .generic_exporter import export_table_to_sheet


def export_all_tables(xml_path: str, wb: Workbook) -> None:
    """
    Creates one sheet per registered table spec and exports rows.
    """
    for _, spec in TABLE_SPECS.items():
        ws = wb.create_sheet(spec["sheet_name"])
        export_table_to_sheet(
            xml_path,
            ws,
            sheet_name=spec["sheet_name"],
            row_tag=spec["row_tag"],
            columns=spec["columns"],
            root_path=spec.get("root_path"),
        )
