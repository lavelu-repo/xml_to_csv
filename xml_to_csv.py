from logging import root
import xml.etree.ElementTree as ET
import csv, os, sys, html, argparse

DEFAULT_COLUMNS = [
    "Record_ID","Source_ID","Pointer","TableConstant","Date","Text",
    "EventIndex","EventDescription","PropertyId","UnitId","UnitTypeId",
    "AgentName","Status","Result","EmployeeId","ShowOnCalendar","iField","VendoreCode"
]

def sanitize(text):
    if text is None:
        return ""
    return html.unescape(text).replace("\n", " ").replace("\r", " ").strip()


def convert_single(inpath, outpath, columns=DEFAULT_COLUMNS):
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        tree = ET.parse("input.xml")
        root = tree.getroot()
        ET.dump(root)
        for event, elem in ET.iterparse(inpath, events=("end",)):
            if elem.tag == "CommonMemo":
                row = {c: "" for c in columns}
                for child in elem:
                    tag = child.tag
                    if tag in row:
                        row[tag] = sanitize(child.text)
                writer.writerow(row)
                elem.clear()

def main():
    p = argparse.ArgumentParser(description="Stream XML CommonMemo -> CSV")
    p.add_argument("source", help="input XML file or directory")
    p.add_argument("dest", nargs="?", help="output CSV file or output directory (optional)")
    args = p.parse_args()

    src = args.source
    dst = args.dest

    if os.path.isdir(src):
        outdir = dst or "output"
        os.makedirs(outdir, exist_ok=True)
        for fname in os.listdir(src):
            if not fname.lower().endswith(".xml"):
                continue
            inpath = os.path.join(src, fname)
            outname = os.path.splitext(fname)[0] + ".csv"
            outpath = os.path.join(outdir, outname)
            print(f"Converting {inpath} -> {outpath}")
            convert_single(inpath, outpath)
    else:
        inpath = src
        if dst:
            outpath = dst
        else:
            base = os.path.splitext(os.path.basename(inpath))[0]
            outpath = os.path.join("formatted", base + ".csv")
            os.makedirs(os.path.dirname(outpath), exist_ok=True)
        print(f"Converting {inpath} -> {outpath}")
        convert_single(inpath, outpath)

if __name__ == "__main__":
    main()