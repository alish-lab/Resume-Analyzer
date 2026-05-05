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

```md
<img width="1195" height="761" alt="image" src="https://github.com/user-attachments/assets/f7e31cea-2770-4285-b17a-b3f7ce27cd7b" />
<img width="1000" height="556" alt="image" src="https://github.com/user-attachments/assets/f105d467-940e-463a-8e27-5e18a818cd8c" />

```

### 2. Add live link (after deployment)

```
 Live Demo: https://your-app.onrender.com
```


Just say 👍
