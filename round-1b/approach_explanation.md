# Round 1B: Approach Explanation

This solution targets Adobe Hackathon 2025 Round 1B: Multi-Collection PDF Analysis. The goal is to analyze a set of PDFs based on a given user persona and a job-to-be-done, then extract and rank relevant content sections and subsections.

We focused entirely on precision, simplicity, and speed, while meeting all resource and runtime constraints.

---

## 🔍 Problem Breakdown

Each test case provides:
- A list of PDF files
- A user persona (e.g., Travel Planner)
- A job (e.g., Plan a trip)
- Expected output: a ranked list of relevant sections and refined subsections

Our output strictly follows the schema defined in `challenge1b_output.json`, with metadata, top sections, and subsection analysis.

---

## 📌 Methodology

### Step 1: Input Parsing
We load the `challenge1b_input.json` to extract:
- Persona
- Job-to-be-done description
- List of PDFs and document titles

The task description is tokenized into lowercase keywords, which guide all subsequent relevance scoring.

### Step 2: PDF Parsing
Using **PyMuPDF**, we extract block-level text from every page of every PDF. PyMuPDF gives precise control over layout and allows for efficient page-wise processing.

All extracted blocks are paired with metadata: page number and document filename.

### Step 3: Section Ranking
Each text block is scored based on how many task-related keywords it contains. The score also considers term frequency and proximity.

We then sort blocks by relevance and return the top 5 as `extracted_sections`, each with:
- Document name
- Page number
- Section title (inferred from heading heuristics or top sentence)
- Importance rank (1–5)

### Step 4: Subsection Analysis
We refine the top-ranked blocks to extract clearer and more concise snippets. These are stored as `subsection_analysis` entries.

Cleaning includes:
- Removing stopwords
- Stripping whitespace and non-informative lines
- Trimming to focus on the part that best addresses the user’s task

---

## 🧠 Why This Approach?

- It's **fast** — easily stays under 60s for 5+ PDFs
- It’s **compliant** — runs fully offline and under 1GB
- It’s **accurate** — keyword-based scoring aligns well with task phrasing
- It’s **simple** — easy to audit and improve if needed

---

## 📦 Constraints Met

- ✅ CPU-only (no GPU dependencies)
- ✅ Model-free (no large ML weights used)
- ✅ Runtime under 60 seconds per collection
- ✅ Docker-based, fully offline execution
- ✅ JSON output schema strictly followed

---

## ✅ Summary

This solution balances lightweight engineering with targeted content extraction. It generalizes well across domains (travel, HR, food), and can be extended further with embedding-based methods if constraints allow.

It’s fast, focused, and reliable — exactly what Round 1B demands.
