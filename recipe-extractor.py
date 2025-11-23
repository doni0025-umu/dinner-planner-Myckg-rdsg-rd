from PIL import Image
import pytesseract
import re
import sys
import os
from pathlib import Path


def extract_recipe(image_path, output_path="recipe_output.txt"):
    if not os.path.exists(image_path):
        print(f"Error: File not found - {image_path}")
        return

    # Open and extract text
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='swe')

    # Split lines and clean up
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    ingredients = []
    instructions = []
    ingredient_pattern = re.compile(r"^(?!\d\.)\d|tsk|msk|ml|gram|g|kg|liter|krm|burk|förp|dl", re.IGNORECASE)

    for line in lines:
        if ingredient_pattern.search(line):
            ingredients.append(line)
        else:
            instructions.append(line)

    # Save to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("INGREDIENTS:\n")
        f.write("\n".join(ingredients))
        f.write("\n\nINSTRUCTIONS:\n")
        f.write("\n".join(instructions))

    print(f"✅ Recipe text saved to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_recipe.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    text_output_path = os.getcwd()+"/recipe_texts/"+Path(sys.argv[1]).stem+".txt"
    extract_recipe(image_path, text_output_path)


