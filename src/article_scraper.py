import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from utils.text_cleaner import clean_text, extract_date
from utils.image_handler import extract_image_info


class ArticleScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_article_content(self, article_url):
        """
        Scrape le contenu complet d'un article à partir de son URL
        """
        try:
            response = requests.get(article_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # structure de l'article
            article_data = {
                'url': article_url,
                'title': None,
                'thumbnail': None,
                'category': None,
                'subcategory': None,
                'summary': None,
                'publication_date': None,
                'author': None,
                'content': None,
                'images': []
            }
            
            # récupérer le titre
            title_tag = soup.find('h1', class_='entry-title')
            if not title_tag:
                title_tag = soup.find('h1')
            article_data['title'] = clean_text(title_tag.get_text()) if title_tag else None
            
            # récupérer thumbnail
            article_tag = soup.find('article')
            if article_tag:
                img_tag = article_tag.find('img', class_='wp-post-image')
                if img_tag:
                    article_data['thumbnail'] = extract_image_info(img_tag)['url']
                else:
                    images = article_tag.find_all('img')
                    if len(images) > 1:
                        article_data['thumbnail'] = extract_image_info(images[1])['url']
                    elif len(images) == 1:
                        article_data['thumbnail'] = extract_image_info(images[0])['url']
            
            # récupérer la catégorie et sous-catégorie
            category_info = self._extract_categories(soup)
            article_data['category'] = category_info['category']
            article_data['subcategory'] = category_info['subcategory']

            # récupérer le résumé/chapô
            entry_content = soup.find('div', class_='entry-content')
            if entry_content:
                first_p = entry_content.find('p')
                if first_p:
                    summary_text = clean_text(first_p.get_text())
                    if summary_text and len(summary_text) > 20:
                        article_data['summary'] = summary_text
            
            # Fallback pour le résumé
            if not article_data['summary']:
                summary_selectors = [
                    soup.find('div', class_='entry-excerpt'),
                    soup.find('div', class_='entry-summary'),
                    soup.find('div', class_='excerpt'),
                    soup.find('p', class_='lead')
                ]
                
                for summary_div in summary_selectors:
                    if summary_div:
                        summary_text = clean_text(summary_div.get_text())
                        if summary_text and len(summary_text) > 20:
                            article_data['summary'] = summary_text
                            break
            
            # Extraire la date de publication
            date_info = self._extract_publication_date(soup)
            article_data['publication_date'] = date_info
            
            # Extraire l'auteur
            article_data['author'] = self._extract_author(soup)
            
            # Extraire le contenu principal
            content_data = self._extract_main_content(soup)
            article_data['content'] = content_data['text']
            article_data['images'] = content_data['images']
            
            return article_data
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors du scraping de {article_url}: {e}")
            return None
        except Exception as e:
            print(f"Erreur inattendue pour {article_url}: {e}")
            return None
    
    def _extract_categories(self, soup):
        """Extrait la catégorie et sous-catégorie"""
        category_info = {'category': None, 'subcategory': None}
        
        # extrait depuis les classes de l'article
        article_tag = soup.find('article')
        if article_tag:
            classes = article_tag.get('class', [])
            for cls in classes:
                if cls.startswith('category-'):
                    category_name = cls.replace('category-', '').replace('-', ' ').title()
                    category_info['category'] = category_name
                    category_info['subcategory'] = category_name 
                    break
        
        # chercher dans la navigation principale
        if not category_info['category']:
            nav = soup.find('nav', class_='main-navigation')
            if nav:
                current_url = soup.find('link', rel='canonical')
                if current_url:
                    url = current_url.get('href', '')
                    if '/web/' in url:
                        category_info['category'] = 'Web'
                    elif '/marketing/' in url:
                        category_info['category'] = 'Marketing'
                    elif '/social/' in url:
                        category_info['category'] = 'Social'
                    elif '/tech/' in url:
                        category_info['category'] = 'Tech'
                    
                    if category_info['category']:
                        category_info['subcategory'] = category_info['category']
        
        # au pire checker dans les breadcrumbs (fallback)
        if not category_info['category']:
            breadcrumb = soup.find('nav', class_='breadcrumb')
            if breadcrumb:
                links = breadcrumb.find_all('a')
                if len(links) >= 2:
                    category_info['category'] = clean_text(links[-2].get_text())
                    category_info['subcategory'] = clean_text(links[-1].get_text())
        
        # ou encore dans les tags de catégorie
        if not category_info['category']:
            cat_tag = soup.find('span', class_='favtag')
            if not cat_tag:
                cat_tag = soup.find('a', rel='category tag')
            if cat_tag:
                category_info['category'] = clean_text(cat_tag.get_text())
                category_info['subcategory'] = category_info['category']  # Par défaut identique
        
        return category_info
    
    def _extract_publication_date(self, soup):
        """Extrait et formate la date de publication au format AAAAMMJJ"""
        
        # structure du site piur la date
        posted_on = soup.find('span', class_='posted-on')
        if posted_on:
            time_element = posted_on.find('time')
            if time_element:
                # via l'attribut datetime
                datetime_attr = time_element.get('datetime')
                if datetime_attr:
                    return extract_date(datetime_attr)
                
                # via le texte
                date_text = time_element.get_text(strip=True)
                if date_text:
                    return extract_date(date_text)
        
        # Fallback: autres sélecteurs possibles
        date_selectors = [
            'time[datetime]',
            '.entry-date',
            'time.published',
            '.date'
        ]
        
        for selector in date_selectors:
            date_element = soup.select_one(selector)
            if date_element:
                # via l'attribut datetime
                datetime_attr = date_element.get('datetime')
                if datetime_attr:
                    return extract_date(datetime_attr)
                
                # via depuis le texte
                date_text = date_element.get_text(strip=True)
                if date_text:
                    return extract_date(date_text)
        
        return None
    
    def _extract_author(self, soup):
        """Extrait l'auteur de l'article"""
        # structure du site pour l'auteur        
        byline = soup.find('span', class_='byline')
        if byline:
            author_link = byline.find('a')
            if author_link:
                # via l'attribut title
                author_name = author_link.get('title')
                if author_name:
                    author_name = clean_text(author_name)
                    if author_name and author_name.lower() not in ['par', 'by', 'author']:
                        return author_name
                
                # via le texte du lien
                author_name = clean_text(author_link.get_text())
                if author_name and author_name.lower() not in ['par', 'by', 'author']:
                    return author_name
        
        # Fallback: autres sélecteurs possibles
        author_selectors = [
            '.author-name',
            '.entry-author',
            '.byline .author',
            'span[class*="author"]',
            '.post-author',
            'a[rel="author"]'
        ]
        
        for selector in author_selectors:
            author_element = soup.select_one(selector)
            if author_element:
                author_name = clean_text(author_element.get_text())
                if author_name and author_name.lower() not in ['par', 'by', 'author']:
                    return author_name
        
        return None
    
    def _extract_main_content(self, soup):
        """Extrait le contenu principal et les images"""
        content_data = {'text': '', 'images': []}
        
        # Chercher la zone de contenu principal
        content_selectors = [
            '.entry-content',
            '.post-content',
            '.article-content',
            'main article',
            '.content'
        ]
        
        content_div = None
        for selector in content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                break
        
        if not content_div:
            print("Zone de contenu principal non trouvée")
            return content_data
        
        # Extraire le texte et nettoyer
        paragraphs = []
        
        # Récupérer tous les paragraphes et éléments de texte
        text_elements = content_div.find_all(['p', 'h2', 'h3', 'h4', 'li', 'blockquote'])
        for element in text_elements:
            text = clean_text(element.get_text())
            if text and len(text) > 10:  # Ignorer les textes très courts
                paragraphs.append(text)
        
        content_data['text'] = '\n\n'.join(paragraphs)
        
        # Extraire toutes les images dans l'ordre d'apparition
        images = content_div.find_all('img')
        for img in images:
            image_info = extract_image_info(img)
            if image_info['url']:
                content_data['images'].append(image_info)
        
        return content_data
