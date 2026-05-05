##  Intelligent Resume–Job Matching System

An NLP-based web application that analyzes resumes against job descriptions and generates a **match score (%)** along with missing skill insights.

---

##  Features

* Resume vs Job Description similarity scoring
* Keyword gap analysis (missing skills detection)
* NLP-based preprocessing using lemmatization and POS tagging
* Regex-based skill/entity extraction
* Clean and simple web interface

---

##  Tech Stack

* Python
* spaCy
* Flask
* Regex
* Scikit-learn (optional for similarity scoring)

---

##  How It Works

1. Text is extracted from resume and job description
2. NLP preprocessing (tokenization, lemmatization, POS tagging)
3. Skill extraction using regex + NLP rules
4. Similarity score is calculated
5. Missing skills are highlighted for improvement

---

##  Output Example

* Match Score: 78%
* Missing Skills: Machine Learning, Docker, APIs

---

##  How to Run

```bash
git clone https://github.com/alish-lab/Resume-Analyzer.git
cd Resume-Analyzer
pip install -r requirements.txt
python app.py
```

---

##  Future Improvements

* Improve semantic matching using transformer models
* Add downloadable report (PDF)
* Deploy as a live web app


### 1. Output Screenshot

<img width="1207" height="787" alt="res" src="https://github.com/user-attachments/assets/7782fa79-406d-40ff-bb52-a7aa1c3d414e" />


### 2. Add live link (after deployment)

```
 Live Demo: https://your-app.onrender.com
```


Just say 👍
