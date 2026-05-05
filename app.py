from flask import Flask, render_template, request
from pathlib import Path
from resume_analyzer import load_spacy_model, clean_text, analyze_resume_text
import PyPDF2

app = Flask(__name__)

nlp = load_spacy_model()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    resume_text = ""
    error = None

    if request.method == "POST":
        resume_text = request.form.get("resume_text", "").strip()
        uploaded_file = request.files.get("resume_file")

        if uploaded_file and uploaded_file.filename:
            filename = uploaded_file.filename.lower()
            try:
                if filename.endswith('.pdf'):
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    resume_text = ""
                    for page in pdf_reader.pages:
                        resume_text += page.extract_text()
                else:
                    raw = uploaded_file.read()
                    resume_text = raw.decode("utf-8", errors="replace")
            except Exception as exc:
                error = f"Could not read uploaded file: {exc}"

        if not resume_text:
            error = error or "Please paste your resume text or upload a .txt or .pdf file."
        else:
            cleaned = clean_text(resume_text)
            if cleaned:
                result = analyze_resume_text(cleaned, nlp)
            else:
                error = "The resume text is empty after cleaning. Please try a different document."

    return render_template("index.html", result=result, resume_text=resume_text, error=error)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
