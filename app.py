import streamlit as st
import json
from datetime import datetime
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import PyPDF2
import docx

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Contract Risk Assessment Bot",
    layout="wide",
    page_icon="📄"
)

# ---------------- HELPERS ----------------
def extract_text(file):
    if file.type == "text/plain":
        return file.read().decode("utf-8")

    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        return "\n".join(page.extract_text() for page in reader.pages)

    if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        return "\n".join(p.text for p in doc.paragraphs)

    return ""

import re

def analyze_risks(text):
    risks = []
    clauses = {}
    score = 0

    t = text.lower()

    # TERMINATION
    if "terminate" in t or "termination" in t:
        if "either party" in t or "both parties" in t:
            score += 5  # fair
        elif "without notice" in t or "any time" in t:
            risks.append("Unilateral termination clause")
            clauses["Termination Clause"] = ("One party can terminate without notice.", 30)
            score += 25
        else:
            score += 15

    # PENALTY / DAMAGES
    if "penalty" in t or "fine" in t:
        amount = re.findall(r"₹\s?\d+[,\d]*", text)
        if amount:
            risks.append("High fixed penalty amount")
            clauses["Penalty Clause"] = ("Fixed monetary penalty imposed.", 30)
            score += 25
        else:
            risks.append("Ambiguous penalty clause")
            clauses["Penalty Clause"] = ("Penalty amount not clearly defined.", 20)
            score += 15

    # JURISDICTION
    if "jurisdiction" in t:
        if "sole" in t or "only" in t:
            risks.append("Jurisdiction favors one party")
            clauses["Jurisdiction Clause"] = ("Jurisdiction is one-sided.", 20)
            score += 15
        else:
            score += 5

    # ARBITRATION
    if "arbitration" not in t:
        risks.append("No arbitration or dispute resolution clause")
        score += 20
    else:
        score -= 5  # good clause

    # NON-COMPETE
    if "non-compete" in t or "not work" in t:
        risks.append("Restrictive non-compete clause")
        score += 20

    return risks, clauses, min(score, 100)

def calculate_risk_score(score):
    return min(max(score, 0), 100)


def risk_badge(score):
    if score <= 30:
        return "🟢 **LOW RISK**"
    elif score <= 60:
        return "🟡 **MEDIUM RISK**"
    else:
        return "🔴 **HIGH RISK**"

def generate_pdf(summary, risks, score):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("<b>Contract Risk Assessment Report</b>", styles["Title"]),
        Paragraph(f"<b>Overall Risk Score:</b> {score}/100", styles["Normal"]),
        Paragraph("<br/>", styles["Normal"]),
        Paragraph("<b>Summary</b>", styles["Heading2"]),
        Paragraph(summary, styles["Normal"]),
        Paragraph("<br/>", styles["Normal"]),
        Paragraph("<b>Key Risks</b>", styles["Heading2"]),
    ]

    for r in risks:
        content.append(Paragraph(f"- {r}", styles["Normal"]))

    doc.build(content)
    buffer.seek(0)
    return buffer

def log_audit(filename, score):
    log = {
        "file": filename,
        "risk_score": score,
        "timestamp": datetime.now().isoformat()
    }
    with open("audit_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")

# ---------------- UI ----------------
st.title("📄 Contract Risk Assessment Bot")
st.caption("AI-powered legal assistant for small & medium businesses")

st.markdown("## 📤 Upload Your Contract")
uploaded_file = st.file_uploader(
    "Drag and drop your contract here",
    type=["txt", "pdf", "docx"]
)

st.caption("Supported formats: TXT, PDF, DOCX • Max 200MB")

if uploaded_file:
    contract_text = extract_text(uploaded_file)

    risks, clauses, raw_score = analyze_risks(contract_text)
    risk_score = calculate_risk_score(raw_score)

    summary = (
        "This contract outlines the agreement between involved parties and defines "
        "obligations, termination conditions, penalties, and jurisdiction. "
        "Some clauses may require legal review."
    )

    log_audit(uploaded_file.name, risk_score)

    col1, col2 = st.columns([2, 1])

    # ---------------- LEFT ----------------
    with col1:
        st.markdown("## 📝 Contract Summary")
        st.info(summary)

        st.markdown("## 📃 Contract Preview")
        st.text_area(
            "Extracted Text (Preview)",
            contract_text[:1500],
            height=260
        )

        st.markdown("## 🔍 Clause Insights")
        for clause, (desc, score) in clauses.items():
            st.markdown(f"**{clause}**")
            st.write(desc)
            st.progress(score)

        st.markdown("## 💡 Suggested Risk Mitigation")
        st.write("✔ Negotiate mutual termination rights")
        st.write("✔ Add penalty caps and clearer definitions")
        st.write("✔ Propose neutral arbitration location")
        st.write("✔ Define clearer performance timelines")

    # ---------------- RIGHT ----------------
    with col2:
        st.markdown("## ⚠️ Risk Assessment")
        st.markdown(risk_badge(risk_score))
        st.metric("📊 Contract Risk Score", f"{risk_score}/100")

        st.markdown("### 🚩 Key Risk Indicators")
        for r in risks:
            st.write("•", r)

        pdf = generate_pdf(summary, risks, risk_score)
        st.download_button(
            "📄 Download Risk Report (PDF)",
            data=pdf,
            file_name="contract_risk_report.pdf",
            mime="application/pdf"
        )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🔒 Contract data is processed locally. No files are stored or shared.")
