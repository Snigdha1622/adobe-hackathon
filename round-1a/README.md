# 📄 Round 1A – PDF Outline Extraction

## 🎯 Objective

Extract a structured outline from PDF documents including:
- Title
- Headings with hierarchy levels (`H1`, `H2`, `H3`)
- Page numbers

The output must follow a strict JSON format and run offline in a containerized environment.

---

## 🧠 Approach

We use a fast, heuristic-based method that:
- Parses each line of the PDF using **PyMuPDF**
- Collects font size, text content, and boldness
- Assigns heading levels (`H1`, `H2`, `H3`) based on the top 3 font sizes
- Extracts the title from the **largest font** text on the first page

This approach avoids machine learning to ensure:
- Fast processing (well under 10 seconds)
- Full offline compatibility
- Minimal memory and CPU usage

### ✅ Multilingual Support

The solution uses Unicode-aware text extraction, allowing it to accurately detect headings in PDFs with Japanese and other non-Latin scripts.

---

## 🧰 Libraries Used

- **Python 3.10**
- **PyMuPDF (fitz)** – for extracting font sizes, positions, and text content

No ML models are used — which ensures speed and compliance with the 200MB constraint.

---

## 📦 How to Build

Run this from the `round-1a/` directory:

```bash
docker build --platform linux/amd64 -t adobe-outline-extractor .
