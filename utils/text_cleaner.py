import re
from datetime import datetime


def clean_text(text):
    """
    Nettoie le texte en supprimant les espaces superflus et caractères indésirables
    """
    if not text:
        return ""
    
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    replacements = {
        '&nbsp;': ' ',
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#8217;': "'",
        '&#8216;': "'",
        '&#8220;': '"',
        '&#8221;': '"',
        '&#8230;': '...',
        '&hellip;': '...',
        '&mdash;': '—',
        '&ndash;': '–'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text.strip()


def extract_date(date_string):
    """
    Extrait et convertit une date au format AAAAMMJJ
    """
    if not date_string:
        return None
    
    date_string = clean_text(date_string)
    
    date_patterns = [
        (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),
        (r'(\d{1,2})/(\d{1,2})/(\d{4})', '%d/%m/%Y'),
        (r'(\d{1,2})-(\d{1,2})-(\d{4})', '%d-%m-%Y'),
        (r'(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})', '%d %B %Y'),
    ]
    
    # Dictionnaire des mois français
    french_months = {
        'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4, 
        'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8, 
        'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
    }
    
    # Essayer chaque pattern
    for pattern, fmt in date_patterns:
        match = re.search(pattern, date_string.lower())
        if match:
            try:
                if fmt == '%Y-%m-%d':
                    year, month, day = match.groups()
                    return f"{year}{month.zfill(2)}{day.zfill(2)}"
                elif fmt in ['%d/%m/%Y', '%d-%m-%Y']:
                    day, month, year = match.groups()
                    return f"{year}{month.zfill(2)}{day.zfill(2)}"
                elif fmt == '%d %B %Y':
                    day, month_name, year = match.groups()
                    if month_name in french_months:
                        month_num = french_months[month_name]
                        return f"{year}{month_num:02d}{int(day):02d}"
            except (ValueError, IndexError):
                continue
    
    # Si aucun pattern ne fonctionne, essayer d'extraire au moins l'année
    year_match = re.search(r'\b(20\d{2})\b', date_string)
    if year_match:
        return f"{year_match.group(1)}0101"  # 1er janvier par défaut
    
    return None


def format_content(content):
    """
    Formate le contenu en ajoutant des retours à la ligne appropriés
    """
    if not content:
        return ""
    
    # sépare les phrases longues
    content = re.sub(r'\.(?=[A-Z])', '.\n', content)
    content = re.sub(r'\.(?=[a-zA-Z])', '. ', content)
    
    # Nettoyer les espaces multiples
    content = re.sub(r'\n+', '\n\n', content)
    content = re.sub(r' +', ' ', content)
    
    return content.strip()


def is_valid_text(text, min_length=10):
    """
    Vérifie si un texte est valide (pas trop court, pas que des espaces, etc.)
    """
    if not text:
        return False
    
    cleaned = clean_text(text)
    
    if len(cleaned) < min_length:
        return False
    
    # check si aucun caractères spéciaux
    if not re.search(r'[a-zA-ZÀ-ÿ]', cleaned):
        return False
    
    return True
