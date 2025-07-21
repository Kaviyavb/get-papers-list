# 📘 PubMed Paper Finder (Aganitha Take-Home Project)

This is a command-line + LLM-style Streamlit web app to fetch **PubMed research papers** that include **non-academic authors** (from pharmaceutical or biotech companies). Built as part of Aganitha’s 2025 Python Take-Home Exercise.

---

## 🚀 Features

- 🔍 Fetch research papers from PubMed API based on any query
- 🧠 Identify non-academic authors using heuristics (e.g., excluding "university", "institute", etc.)
- 📊 Download filtered results as a CSV
- 💬 Beautiful LLM-style web UI built using Streamlit
- 🖥️ Also includes a CLI interface via Poetry
- ✅ LLM-assisted development using ChatGPT (link below)

---

## 📦 Project Structure

get-papers-list/
├── app.py ← Streamlit UI
├── get-papers-list.py ← CLI interface
├── get_papers_list/
│ ├── init.py
│ └── fetcher.py ← All backend logic
├── README.md
├── pyproject.toml
