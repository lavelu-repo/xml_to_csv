import xml.etree.ElementTree as ET
from collections import defaultdict
import json, os
import logging

logger = logging.getLogger(__name__)

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

def old_save_nested_structure_as_json(
    xml_path: str,
    max_depth: int,
    max_per_tag_per_level: int = 2,
    strip_ns: bool = True,
) -> None:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Key: (depth, path_tuple) -> counts per tag under that parent path
    printed = defaultdict(lambda: defaultdict(int))

    def build(elem, depth, path):
        if depth > max_depth:
            return None

        tag = strip_namespace(elem.tag) if strip_ns else elem.tag

        # Limit per (depth + parent path), not globally per depth
        key = (depth, tuple(path))
        if printed[key][tag] >= max_per_tag_per_level:
            return None
        printed[key][tag] += 1

        children = list(elem)
        if not children:
            return {tag: ""}

        if depth >= max_depth:
            return {tag: {}}

        node_obj = {}
        next_path = path + [tag]

        for child in children:
            child_node = build(child, depth + 1, next_path)
            if child_node:
                # keep first occurrence of each child tag in this structure view
                for k, v in child_node.items():
                    if k not in node_obj:
                        node_obj[k] = v

        return {tag: node_obj if node_obj else {}}

    structure = build(root, 0, [])

    base = os.path.splitext(os.path.basename(xml_path))[0]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"{base}_structure.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2)

    print(f"✅ Structure JSON written to: {out_path}")


def save_nested_structure_as_json(
    xml_path: str,
    max_depth: int,
    max_per_tag_per_level: int = 2,
    strip_ns: bool = True,
) -> None:
    logger.info("Building structure for %s (max_depth=%d)", xml_path, max_depth)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Count tags per (depth, parent_path) so limits don't block other sections
    printed = defaultdict(lambda: defaultdict(int))

    def build(elem, depth, path):
        if depth > max_depth:
            return None

        tag = strip_namespace(elem.tag) if strip_ns else elem.tag

        # Limit per parent path at this depth (not global per depth)
        key = (depth, tuple(path))
        if printed[key][tag] >= max_per_tag_per_level:
            return None
        printed[key][tag] += 1

        children = list(elem)
        if not children:
            return {tag: ""}

        if depth >= max_depth:
            return {tag: {}}

        node_obj = {}
        next_path = path + [tag]

        for child in children:
            child_node = build(child, depth + 1, next_path)
            if not child_node:
                continue

            # child_node is a dict with a single key: {childTag: childValue}
            for k, v in child_node.items():
                if k not in node_obj:
                    node_obj[k] = v
                else:
                    # If the same child tag repeats, store as array
                    if not isinstance(node_obj[k], list):
                        node_obj[k] = [node_obj[k]]
                    node_obj[k].append(v)

        return {tag: node_obj if node_obj else {}}

    structure = build(root, 0, [])

    base = os.path.splitext(os.path.basename(xml_path))[0]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"{base}_structure.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2)

    logger.info("✅ Structure JSON written to: %s", out_path)