# Contract Analysis \& Risk Assessment Bot


# 📄 Contract Analysis & Risk Assessment Bot

Ever read a contract and thought  
“🙂 okay…”  
“🤨 wait what?”  
“😨 WHY is this even legal??”

Yeah. Same.

This project is a **GenAI-inspired Contract Risk Assessment Bot** built to help **small and medium businesses (SMEs)** understand complex contracts *without needing a law degree*.

---

## 🚀 What Does This Do?

You upload a contract.  
The bot:
- Reads it 📖
- Breaks it down 🧠
- Finds risky clauses 🚩
- Scores the contract ⚠️
- Explains everything in **plain business language**
- Suggests how to fix the risks 💡

All **locally processed**.  
No data leaks. No uploads to the cloud. No stress. 🔒

---

## ✨ Features

✔ Upload contracts in **TXT, PDF, DOCX**  
✔ Clause-level risk detection  
✔ Overall risk score (0–100)  
✔ Color-coded risk level (Low / Medium / High)  
✔ Plain-English contract summary  
✔ Risk mitigation suggestions  
✔ Downloadable **PDF risk report**  
✔ Local **audit log** for traceability  
✔ Supports **English & Hindi contracts**  
✔ Simple, clean & judge-friendly UI  

---

## 🧠 How It Works (In Simple Words)

Instead of blindly flagging keywords, the system:
- Checks **clause fairness**
- Detects **one-sided termination**
- Identifies **heavy or ambiguous penalties**
- Flags **jurisdiction bias**
- Penalizes missing **arbitration/dispute resolution**

The risk score changes **based on severity**, not just word presence.

Smart. Explainable. Practical.

---

## 🛠 Tech Stack

- Python 🐍  
- Streamlit 🎈  
- Rule-based NLP logic  
- ReportLab (PDF generation)  
- JSON-based audit logging  

No external legal databases.  
No paid APIs.  
Fully compliant with hackathon constraints.

---

## ▶️ How To Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
