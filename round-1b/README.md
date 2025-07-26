# Challenge 1B: Multi-Collection PDF Analysis

## Overview

This solution handles multi-document PDF analysis tailored to different user personas and goals. It processes collections of PDFs and returns ranked sections and refined subsections that match the user’s task.

The solution runs in a Docker container, works offline, and produces JSON outputs that conform to the provided schema.

---

## 🔧 Folder Structure

```
round-1b/
├── Collection_1_Travel/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection_2_Acrobat/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection_3_Recipes/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── analyzer.py
├── Dockerfile
└── README.md
```

---

## 📦 How to Build

> From inside the `round-1b/` folder:

```bash
docker build --platform linux/amd64 -t adobe-analyzer .
```

---

## 🚀 How to Run

**Windows PowerShell:**

```powershell
docker run --rm `
  -v "${PWD}\:/app" `
  --network none `
  adobe-analyzer
```

**Linux/macOS:**

```bash
docker run --rm -v "$(pwd):/app" --network none adobe-analyzer
```

---

## 📤 Output

Each collection folder (`Collection_1_Travel`, `Collection_2_Acrobat`, etc.) will be updated with a `challenge1b_output.json` file that contains:

- `extracted_sections`: Ranked sections most relevant to the persona's task
- `subsection_analysis`: Refined, cleaned snippets for each top section

These outputs follow the schema defined in the challenge documentation.

---

## 🧠 Libraries and Techniques

- [`PyMuPDF`](https://github.com/pymupdf/PyMuPDF) for fast, reliable PDF parsing
- Lightweight keyword scoring instead of ML/LLMs (for performance compliance)
- Runs entirely offline, inside a Docker container, under strict resource limits

---

## ✅ Compliance Checklist

- [x] Processes all collections automatically
- [x] Outputs valid JSON per schema
- [x] Runs offline in < 200MB image
- [x] Completes execution within time/memory limits
- [x] No internet or external API dependencies
- [x] Dockerfile provided and tested

---

## 📎 See Also

- [`approach_explanation.md`](./approach_explanation.md) – for technical write-up and scoring focus
