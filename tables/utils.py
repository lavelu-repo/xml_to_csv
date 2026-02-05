import xml.etree.ElementTree as ET

def strip_namespace(tag: str) -> str:
    # "{urn:...}CommProperty" -> "CommProperty"
    return tag.split("}", 1)[1] if "}" in tag else tag

def safe_text(text: str | None) -> str:
    return (text or "").strip()
