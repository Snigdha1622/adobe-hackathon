import os
import fitz  # PyMuPDF
import json
from collections import Counter

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    font_info = []

    outline = []
    possible_headings = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                line_text = ""
                font_sizes = []
                is_bold = False
                for span in line["spans"]:
                    if not span["text"].strip():
                        continue
                    line_text += span["text"]
                    font_sizes.append(span["size"])
                    if "Bold" in span["font"]:
                        is_bold = True

                if line_text.strip():
                    avg_size = sum(font_sizes) / len(font_sizes)
                    possible_headings.append({
                        "text": line_text.strip(),
                        "size": round(avg_size, 2),
                        "bold": is_bold,
                        "page": page_num + 1
                    })

    # Detect most common sizes
    sizes = [h["size"] for h in possible_headings]
    top_sizes = [size for size, _ in Counter(sizes).most_common()]

    # Assign H1, H2, H3 based on size rank
    size_to_level = {}
    for idx, size in enumerate(sorted(top_sizes, reverse=True)[:3]):
        size_to_level[size] = f"H{idx+1}"

    for h in possible_headings:
        level = size_to_level.get(h["size"])
        if level:
            outline.append({
                "level": level,
                "text": h["text"],
                "page": h["page"]
            })

    # Pick title: largest size text on first page, centered
    title = ""
    first_page = doc[0]
    blocks = first_page.get_text("dict")["blocks"]
    max_size = 0

    for b in blocks:
        if "lines" not in b:
            continue
        for line in b["lines"]:
            for span in line["spans"]:
                if not span["text"].strip():
                    continue
                if span["size"] > max_size and abs(span["bbox"][0] - span["bbox"][2]) < first_page.rect.width * 0.8:
                    max_size = span["size"]
                    title = span["text"].strip()

    return {
        "title": title,
        "outline": outline
    }

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            result = extract_outline(pdf_path)

            json_filename = os.path.splitext(filename)[0] + ".json"
            json_path = os.path.join(output_dir, json_filename)

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
