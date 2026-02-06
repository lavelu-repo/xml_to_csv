import sys
sys.dont_write_bytecode = True

import os, argparse
from openpyxl import Workbook
import logging

from logging_config import setup_logging
from structure.printer import save_nested_structure_as_json
from tables.export_all import export_all_tables


INPUT_DIR = "input"
OUTPUT_DIR = "output"

def main():
    p = argparse.ArgumentParser(description="XML → Excel (one sheet per table)")
    p.add_argument("filename", help="XML filename only (in input/)")
    p.add_argument("--log-level", help="Override log level (DEBUG/INFO/WARNING)", default=None)
    p.add_argument("--print-structure", action="store_true",
                   help="Print nested XML structure and exit")
    p.add_argument("--max-depth", type=int, default=1,
                   help="Max depth for --print-structure")
    p.add_argument("--max-per-tag-per-level", type=int, default=2,
                   help="Max occurrences per tag per level")

    args = p.parse_args()

    # configure logging from env or CLI
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    xml_path = os.path.join(INPUT_DIR, args.filename)
    logger.info("Starting processing for %s", args.filename)
    if not os.path.isfile(xml_path):
        logger.error("Input file not found: %s", xml_path)
        raise SystemExit(f"❌ Input file not found: {xml_path}")

    if args.print_structure:
        logger.info(
            "Printing nested structure for %s (max_depth=%d, max_per_tag_per_level=%d)",
            xml_path,
            args.max_depth,
            args.max_per_tag_per_level,
        )
        save_nested_structure_as_json(
            xml_path,
            max_depth=args.max_depth,
            max_per_tag_per_level=args.max_per_tag_per_level,
        )

        logger.info("Done printing structure for %s", xml_path)
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(
        OUTPUT_DIR, os.path.splitext(args.filename)[0] + ".xlsx"
    )

    wb = Workbook()
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

    logger.info("Exporting tables from %s -> %s", xml_path, out_path)
    export_all_tables(xml_path, wb)

    wb.save(out_path)
    logger.info("✅ Excel written to: %s", out_path)

if __name__ == "__main__":
    main()
