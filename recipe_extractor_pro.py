import json
import re
import difflib
from pathlib import Path

import cv2
from paddleocr import PPStructureV3


# -------------------------------------------------------------
# CONSTANTS
# -------------------------------------------------------------

INGREDIENT_TITLES = [
    "ingredienser", "ingredient", "ingredients", "ingridienser",
    "ingredienter", "ingredienslista", "lista"
]

INSTRUCTION_TITLES = [
    "instruktioner", "instructions", "gör så här",
    "how to", "tillagning", "metod", "method"
]

SWEDISH_UNITS = [
    "g", "gram", "kg", "ml", "dl", "l", "liter",
    "msk", "tsk", "krm", "st", "pkt", "förp"
]

QUANTITY_REGEX = r"(?P<quantity>(?:\d+(?:[\.,]\d+)?)\s*\w*|½|¼|¾|en|ett|några)?"


# -------------------------------------------------------------
# FUZZY MATCHING HELPERS
# -------------------------------------------------------------

def fuzzy_equals(a, b, threshold=0.75):
    return difflib.SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio() >= threshold


def matches_any(text, keywords):
    txt = text.lower().strip()
    return any(fuzzy_equals(txt, k) or txt.startswith(k) for k in keywords)


# -------------------------------------------------------------
# SECTION EXTRACTION (UPDATED FOR PPStructureV3)
# -------------------------------------------------------------

def extract_sections(blocks):
    ingredients = []
    instructions = []
    section = None

    for blk in blocks:
        if blk.get("type") != "text":
            continue

        text = blk.get("text", "").strip()
        low = text.lower()

        # Section detection
        if matches_any(low, INGREDIENT_TITLES):
            section = "ingredients"
            continue

        if matches_any(low, INSTRUCTION_TITLES):
            section = "instructions"
            continue

        # Ingredient lines
        if section == "ingredients" and is_ingredient_line(text):
            ingredients.append(text)

        # Instruction lines
        elif section == "instructions":
            instructions.append(text)

    return ingredients, instructions


def is_ingredient_line(t):
    t = t.lower()

    if any(unit in t for unit in SWEDISH_UNITS):
        return True

    if re.match(r"^\d+", t):
        return True

    if re.search(r"\d+/\d+", t):
        return True

    return False


# -------------------------------------------------------------
# PARSER
# -------------------------------------------------------------

def parse_ingredient(line):
    pattern = rf"{QUANTITY_REGEX}\s*(?P<item>.+)"
    m = re.match(pattern, line.strip(), re.IGNORECASE)
    if not m:
        return {"item": line, "quantity": ""}
    return {
        "item": m.group("item").strip(),
        "quantity": (m.group("quantity") or "").strip()
    }


# -------------------------------------------------------------
# MAIN EXTRACTION USING PPStructureV3
# -------------------------------------------------------------

def extract_recipe(image_path):
    img_path = Path(image_path)
    img = cv2.imread(str(img_path))

    print(f"🔍 Processing: {img_path.name}")

    engine = PPStructureV3()

    # OCR + Layout
    blocks = engine(img)

    # Sort blocks for multi-column documents
    blocks.sort(key=lambda b: (b["bbox"][1], b["bbox"][0]))

    # Extract sections
    ing_raw, inst_raw = extract_sections(blocks)

    ingredients = [parse_ingredient(i) for i in ing_raw]

    recipe_json = {
        "name": img_path.stem.replace("_", " ").title(),
        "ingredients": ingredients,
        "instructions": inst_raw
    }

    # Save JSON
    out_path = img_path.with_suffix(".json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(recipe_json, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved: {out_path}\n")
    return recipe_json


# -------------------------------------------------------------
# PROCESS A WHOLE FOLDER
# -------------------------------------------------------------

def process_folder(folder):
    folder = Path(folder)
    images = [*folder.glob("*.jpg"), *folder.glob("*.png"), *folder.glob("*.jpeg")]

    if not images:
        print("⚠️ No images found.")
        return

    for img in images:
        extract_recipe(img)


# -------------------------------------------------------------
# CLI
# -------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python recipe_extractor_v3.py <image_path>")
        print("  python recipe_extractor_v3.py <folder>")
        sys.exit(0)

    target = Path(sys.argv[1])

    if target.is_file():
        extract_recipe(target)
    elif target.is_dir():
        process_folder(target)
    else:
        print("❌ Invalid path")
