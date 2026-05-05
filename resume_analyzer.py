import argparse
import csv
import os
import re
import sys
from pathlib import Path

COMMON_RESUME_SKILLS = [
    "accounting", "analytics", "analysis", "benefits", "billing", "budgeting",
    "customer service", "data analysis", "employee relations", "finance",
    "human resources", "insurance", "leadership", "management", "marketing",
    "marketing collateral", "medical billing", "medical terminology", "office",
    "operations", "performance reviews", "policies", "presentations", "project management",
    "public relations", "purchasing", "reporting", "research", "sales",
    "social media", "staff training", "strategic planning", "team management",
    "training and development", "vendor management", "workflow", "written communication",
    "customer satisfaction", "conflict resolution", "budget management", "quality assurance"
]

ACTION_VERBS = {
    "achieve", "build", "create", "design", "develop", "drive", "enhance", "execute",
    "improve", "implement", "manage", "lead", "organize", "plan", "reduce", "resolve",
    "streamline", "support", "train", "build", "increase", "analyze", "prepare",
    "deliver", "coordinate", "supervise", "deliver", "monitor", "execute"
}

SECTION_KEYWORDS = {
    "summary": ["summary", "objective", "profile"],
    "experience": ["experience", "employment", "work history", "professional experience"],
    "skills": ["skills", "technical skills", "core skills", "strengths"],
    "education": ["education", "academic", "certification", "certifications"]
}


def load_spacy_model():
    try:
        import spacy
    except ImportError as exc:
        raise SystemExit(
            "spaCy is not installed. Install it with `pip install -r requirements.txt` and try again."
        ) from exc

    model_name = "en_core_web_sm"
    try:
        return spacy.load(model_name)
    except OSError:
        from spacy.cli import download

        print(f"Downloading spaCy model {model_name}...")
        download(model_name)
        return spacy.load(model_name)


def clean_text(text: str) -> str:
    if text is None:
        return ""
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def has_section(text: str, section: str) -> bool:
    lower = text.lower()
    for keyword in SECTION_KEYWORDS.get(section, []):
        if re.search(rf"\b{re.escape(keyword)}\b", lower):
            return True
    return False


def extract_skills(text: str) -> set[str]:
    lower = text.lower()
    matches = set()
    for skill in COMMON_RESUME_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", lower):
            matches.add(skill)
    return matches


def count_action_verbs(doc) -> int:
    count = 0
    for token in doc:
        if token.pos_ == "VERB" and token.lemma_.lower() in ACTION_VERBS:
            count += 1
    return count


def score_resume(text: str, doc) -> tuple[int, dict]:
    clean = clean_text(text)
    word_count = len([token for token in doc if not token.is_punct and not token.is_space])
    sentence_count = max(1, len(list(doc.sents)))

    summary_present = has_section(clean, "summary")
    experience_present = has_section(clean, "experience")
    skills_present = has_section(clean, "skills")
    education_present = has_section(clean, "education")

    found_skills = extract_skills(clean)
    action_count = count_action_verbs(doc)
    action_ratio = action_count / sentence_count

    score_detail = {
        "word_count": word_count,
        "sentences": sentence_count,
        "summary": summary_present,
        "experience": experience_present,
        "skills_section": skills_present,
        "education": education_present,
        "matched_skills": len(found_skills),
        "action_verbs": action_count,
        "action_ratio": round(action_ratio, 2),
    }

    summary_score = 20 if summary_present else 5
    section_score = 15 if experience_present and skills_present and education_present else 6
    skill_score = min(25, int(25 * len(found_skills) / 10))
    action_score = min(25, int(25 * min(action_ratio / 0.4, 1.0)))

    if 180 <= word_count <= 650:
        length_score = 15
    else:
        penalty = min(15, abs(word_count - 400) // 30)
        length_score = max(0, 15 - penalty)

    total = summary_score + section_score + skill_score + action_score + length_score
    return min(100, total), score_detail


def suggest_improvements(text: str, doc, score_detail: dict) -> list[str]:
    suggestions: list[str] = []
    sample = clean_text(text)

    if not score_detail["summary"]:
        suggestions.append("Add a clear professional summary or objective at the top.")
    if score_detail["matched_skills"] < 8:
        suggestions.append(
            "List more industry-relevant skills and tools, especially the ones your target job requires."
        )
    if score_detail["action_ratio"] < 0.4:
        suggestions.append(
            "Use more strong action verbs to describe your accomplishments and responsibilities."
        )
    if score_detail["word_count"] > 700:
        suggestions.append("Trim the resume to two pages by removing repetitive details and focusing on accomplishments.")
    if score_detail["word_count"] < 180:
        suggestions.append("Expand the resume with more details about results, responsibilities, and relevant achievements.")
    if not score_detail["education"]:
        suggestions.append("Include an education section with degrees, certificates, or relevant coursework.")
    if not score_detail["experience"]:
        suggestions.append("Add an experience section with job titles, company names, dates, and measurable results.")
    if score_detail["skills_section"] is False and score_detail["matched_skills"] > 0:
        suggestions.append("Create a dedicated skills section so recruiters can find your strengths quickly.")

    if len(suggestions) == 0:
        suggestions.append("Your resume looks balanced. Keep the strong structure and focus on measurable results.")

    return suggestions


def analyze_resume_text(text: str, nlp) -> dict:
    doc = nlp(text)
    score, details = score_resume(text, doc)
    suggestions = suggest_improvements(text, doc, details)
    detalles = {
        "score": score,
        "details": details,
        "suggestions": suggestions,
        "skills_found": sorted(extract_skills(clean_text(text)))
    }
    return detalles


def load_resumes(file_path: Path, limit: int | None = None) -> list[dict[str, str]]:
    rows = []
    with file_path.open("r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            rows.append(row)
            if limit is not None and i + 1 >= limit:
                break
    return rows


def print_analysis(row: dict[str, str], result: dict) -> None:
    print("=" * 72)
    print(f"Resume ID: {row.get('ID', 'unknown')}")
    print(f"Category: {row.get('Category', 'unknown')}\n")
    print(f"Resume score: {result['score']} / 100")
    print("Details:")
    for key, value in result["details"].items():
        print(f"  - {key}: {value}")
    if result["skills_found"]:
        print(f"  - skills found: {', '.join(result['skills_found'][:15])}")
    print("\nSuggestions:")
    for suggestion in result["suggestions"]:
        print(f"  - {suggestion}")
    print("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple AI resume analyzer using spaCy.")
    parser.add_argument("--file", default="Resume.csv", help="CSV file containing resume data.")
    parser.add_argument("--limit", type=int, default=3, help="Number of resumes to analyze.")
    parser.add_argument("--id", help="Analyze only the resume with this ID.")
    args = parser.parse_args()

    resume_path = Path(args.file)
    if not resume_path.exists():
        raise SystemExit(f"File not found: {resume_path}")

    nlp = load_spacy_model()
    resumes = load_resumes(resume_path, limit=None if args.id else args.limit)

    selected = []
    for row in resumes:
        if args.id and row.get("ID") != args.id:
            continue
        selected.append(row)

    if not selected:
        raise SystemExit("No resumes found to analyze.")

    for row in selected:
        text = clean_text(row.get("Resume_str", ""))
        if not text:
            print(f"Skipping resume ID {row.get('ID')} because text is missing.")
            continue
        result = analyze_resume_text(text, nlp)
        print_analysis(row, result)


if __name__ == "__main__":
    main()
