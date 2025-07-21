def extract_image_info(img_tag):
    """
    Extrait les informations d'une image (URL et légende/description)
    """
    if not img_tag:
        return {'url': None, 'caption': None}
    
    # exitraire l'URL de l'image
    url = extract_img_url(img_tag)
    
    # et la légende/description
    caption = extract_image_caption(img_tag)
    
    return {
        'url': url,
        'caption': caption
    }


def extract_img_url(img_tag):
    """
    Extrait l'URL d'une image en vérifiant plusieurs attributs possibles
    """
    if not img_tag:
        return None
    
    # attribut possible
    url_attributes = [
        'data-lazy-src',   
        'data-src',         
        'data-original',    
        'src'               
    ]
    
    for attr in url_attributes:
        if img_tag.has_attr(attr):
            url = img_tag[attr]
            if url and (url.startswith('http') or url.startswith('//')):
                if url.startswith('//'):
                    url = 'https:' + url
                return url
    
    return None


def extract_image_caption(img_tag):
    """
    Extrait la légende ou description d'une image
    """
    if not img_tag:
        return None
    
    caption_sources = []
    
    # attribut alt de l'image
    if img_tag.has_attr('alt'):
        alt_text = img_tag['alt'].strip()
        if alt_text and alt_text.lower() not in ['image', 'photo', 'picture']:
            caption_sources.append(alt_text)
    
    # attribut title de l'image
    if img_tag.has_attr('title'):
        title_text = img_tag['title'].strip()
        if title_text and title_text not in caption_sources:
            caption_sources.append(title_text)
    
    # chercher une légende dans les éléments parents/suivants
    parent = img_tag.parent
    if parent:
        figcaption = parent.find('figcaption')
        if figcaption:
            caption_text = figcaption.get_text(strip=True)
            if caption_text and caption_text not in caption_sources:
                caption_sources.append(caption_text)
        
        caption_elem = parent.find(class_=lambda x: x and 'caption' in x.lower())
        if caption_elem:
            caption_text = caption_elem.get_text(strip=True)
            if caption_text and caption_text not in caption_sources:
                caption_sources.append(caption_text)
    
    # chercher dans le contexte proche (éléments suivants)
    next_elem = img_tag.find_next_sibling(['p', 'span', 'div'])
    if next_elem:
        text = next_elem.get_text(strip=True)
        if text and len(text) < 200:  
            classes = next_elem.get('class', [])
            if any('caption' in str(cls).lower() or 'legend' in str(cls).lower() for cls in classes):
                if text not in caption_sources:
                    caption_sources.append(text)
    
    # retourne la première légende trouvée 
    return caption_sources[0] if caption_sources else None


def is_valid_image_url(url):
    """
    Vérifie si une URL d'image est valide
    """
    if not url:
        return False
    
    # vérifie que c'est bien une URL
    if not (url.startswith('http') or url.startswith('//')):
        return False
    
    # vérifie les extensions d'image courantes
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp']
    url_lower = url.lower()
    
    # url finit par extensin 
    if any(url_lower.endswith(ext) for ext in image_extensions):
        return True
    
    if any(ext in url_lower for ext in image_extensions):
        return True
    
    exclude_patterns = ['javascript:', 'data:text', 'mailto:', '.pdf', '.doc']
    if any(pattern in url_lower for pattern in exclude_patterns):
        return False
    
    return True


def clean_image_url(url):
    """
    Nettoie une URL d'image
    """
    if not url:
        return None
    
    url = url.strip()
    
    # url relativ
    if url.startswith('//'):
        url = 'https:' + url
    elif url.startswith('/') and not url.startswith('//'):
        url = 'https://www.blogdumoderateur.com' + url
    
    if '?' in url:
        base_url, params = url.split('?', 1)
        important_params = ['w=', 'h=', 'quality=', 'format=']
        if any(param in params for param in important_params):
            return url
        else:
            return base_url
    
    return url
