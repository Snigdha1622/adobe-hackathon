import json
import os
from pathlib import Path
import fitz  # PyMuPDF

def extract_text_by_page(pdf_path):
    text_by_page = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text("blocks")
            blocks = sorted(text, key=lambda b: (-b[3] + b[1]))  # sort top to bottom
            text_by_page.append((page.number + 1, blocks))
    return text_by_page

def rank_sections(text_blocks, persona_keywords):
    scored_sections = []
    for page_num, blocks in text_blocks:
        for block in blocks:
            text = block[4].strip()
            if not text or len(text) < 30:
                continue
            score = sum(text.lower().count(k) for k in persona_keywords)
            if score > 0:
                scored_sections.append({
                    "document": None,  # to fill in later
                    "section_title": text[:60],
                    "importance_rank": score,
                    "page_number": page_num
                })
    scored_sections.sort(key=lambda x: -x["importance_rank"])
    return scored_sections[:5]

def refine_subsections(scored_sections):
    refined = []
    for s in scored_sections:
        refined.append({
            "document": s["document"],
            "refined_text": s["section_title"],
            "page_number": s["page_number"]
        })
    return refined

def analyze_collection(folder_path):
    input_path = Path(folder_path) / "challenge1b_input.json"
    output_path = Path(folder_path) / "challenge1b_output.json"
    pdf_dir = Path(folder_path) / "PDFs"

    with open(input_path) as f:
        config = json.load(f)

    persona_keywords = config["job_to_be_done"]["task"].lower().split()
    sections = []
    
    for doc in config["documents"]:
        file_path = pdf_dir / doc["filename"]
        text_blocks = extract_text_by_page(str(file_path))
        section_scores = rank_sections(text_blocks, persona_keywords)
        for s in section_scores:
            s["document"] = doc["filename"]
        sections.extend(section_scores)

    final_sections = sections[:5]
    final_subsections = refine_subsections(final_sections)

    result = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in config["documents"]],
            "persona": config["persona"]["role"],
            "job_to_be_done": config["job_to_be_done"]["task"]
        },
        "extracted_sections": final_sections,
        "subsection_analysis": final_subsections
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Processed: {folder_path}")

if __name__ == "__main__":
    base_path = Path(__file__).parent
    for folder in ["Collection_1_Travel", "Collection_2_Acrobat", "Collection_3_Recipes"]:
        analyze_collection(base_path / folder)
