"""Resume PDF analyzer that extracts and scores resume content."""

import re

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None


IMPORTANT_SECTIONS = [
    'education', 'experience', 'skills', 'projects',
    'certifications', 'achievements', 'internships', 'summary',
]

TECH_KEYWORDS = [
    'python', 'java', 'javascript', 'react', 'django', 'flask', 'node',
    'sql', 'html', 'css', 'git', 'docker', 'aws', 'linux', 'c++',
    'machine learning', 'data science', 'tensorflow', 'pytorch',
    'rest api', 'mongodb', 'postgresql', 'kubernetes', 'ci/cd',
    'agile', 'scrum', 'typescript', 'angular', 'vue', 'spring',
]


def extract_text_from_pdf(file_obj):
    if PdfReader is None:
        return ''
    reader = PdfReader(file_obj)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text


def analyze_resume(file_obj):
    text = extract_text_from_pdf(file_obj)
    text_lower = text.lower()

    result = {
        'score': 0,
        'suggestions': [],
        'skills_found': [],
        'sections_found': [],
        'missing_sections': [],
    }

    if not text.strip():
        result['suggestions'].append('Could not extract text from PDF. Ensure it is not image-based.')
        return result

    score = 0

    # Check sections
    for section in IMPORTANT_SECTIONS:
        if section in text_lower:
            result['sections_found'].append(section.title())
            score += 8
        else:
            result['missing_sections'].append(section.title())

    # Check tech keywords
    for keyword in TECH_KEYWORDS:
        if keyword in text_lower:
            result['skills_found'].append(keyword.title())
            score += 2

    # Check for links
    if 'github' in text_lower or 'github.com' in text_lower:
        score += 5
    else:
        result['suggestions'].append('Add your GitHub profile link to showcase your code.')

    if 'linkedin' in text_lower or 'linkedin.com' in text_lower:
        score += 5
    else:
        result['suggestions'].append('Add your LinkedIn profile link for professional networking.')

    # Check for measurable achievements
    numbers = re.findall(r'\d+%|\d+\+|\$\d+', text)
    if numbers:
        score += 10
    else:
        result['suggestions'].append('Add measurable achievements (e.g., "Improved performance by 30%").')

    # Check for contact info
    email_pattern = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    if email_pattern:
        score += 5
    else:
        result['suggestions'].append('Include your email address.')

    phone_pattern = re.findall(r'\+?\d[\d\s-]{8,}\d', text)
    if phone_pattern:
        score += 5
    else:
        result['suggestions'].append('Include your phone number.')

    # Missing section suggestions
    if 'Projects' in result['missing_sections']:
        result['suggestions'].append('Add a Projects section to showcase your practical work.')
    if 'Internships' in result['missing_sections']:
        result['suggestions'].append('Add internship experience if you have any.')
    if 'Certifications' in result['missing_sections']:
        result['suggestions'].append('Add relevant certifications to strengthen your profile.')

    # Length check
    word_count = len(text.split())
    if word_count < 150:
        result['suggestions'].append('Your resume seems too short. Add more details about your experience.')
    elif word_count > 800:
        result['suggestions'].append('Your resume might be too long. Try to keep it concise (1-2 pages).')

    result['score'] = min(score, 100)
    return result
