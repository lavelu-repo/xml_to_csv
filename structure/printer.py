import xml.etree.ElementTree as ET
from collections import defaultdict
import json, os

OUTPUT_DIR = "output"

def strip_namespace(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag

def print_nested_tags_with_limits(
    xml_path: str,
    max_depth: int,
    max_per_tag_per_level: int = 2,
    strip_ns: bool = True,
) -> None:
    """
    Print XML as a nested structure with opening/closing tags.
    Enforces: max N occurrences PER TAG per level.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    printed = defaultdict(lambda: defaultdict(int))

    def walk(elem, depth):
        if depth > max_depth:
            return

        tag = strip_namespace(elem.tag) if strip_ns else elem.tag

        if printed[depth][tag] >= max_per_tag_per_level:
            return
        printed[depth][tag] += 1

        indent = "  " * depth
        children = list(elem)

        if depth < max_depth and children:
            print(f"{indent}<{tag}>")
            for child in children:
                walk(child, depth + 1)
            print(f"{indent}</{tag}>")
        else:
            print(f"{indent}<{tag}></{tag}>")

    walk(root, 0)


def save_nested_structure_as_json(
    xml_path: str,
    max_depth: int,
    max_per_tag_per_level: int = 2,
    strip_ns: bool = True,
) -> None:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    printed = defaultdict(lambda: defaultdict(int))

    def build(elem, depth):
        if depth > max_depth:
            return None

        tag = strip_namespace(elem.tag) if strip_ns else elem.tag

        if printed[depth][tag] >= max_per_tag_per_level:
            return None
        printed[depth][tag] += 1

        children = list(elem)
        has_children = len(children) > 0

        # Leaf element => ""
        if not has_children:
            return {tag: ""}

        # Has children but we're at the depth limit => show container, but don't expand
        if depth >= max_depth:
            return {tag: {}}

        # Expand children
        node_obj = {}
        for child in children:
            child_node = build(child, depth + 1)
            if child_node:
                node_obj.update(child_node)

        return {tag: node_obj if node_obj else {}}

    structure = build(root, 0)

    base = os.path.splitext(os.path.basename(xml_path))[0]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"{base}_structure.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2)

    print(f"✅ Structure JSON written to: {out_path}")