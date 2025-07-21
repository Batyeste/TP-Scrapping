import requests
from bs4 import BeautifulSoup
from utils.image_handler import extract_image_info


class ListScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_articles_list(self, url, max_pages=1):
        """
        Récupère la liste des articles depuis les pages de catégories
        """
        articles_urls = []
        
        for page in range(1, max_pages + 1):
            page_url = f"{url}/page/{page}" if page > 1 else url
            print(f"Scraping page {page}: {page_url}")
            
            try:
                response = requests.get(page_url, headers=self.headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # trouver tous les articles sur la page
                articles = self._extract_articles_from_page(soup)
                
                if not articles:
                    print(f"Aucun article trouvé sur la page {page}")
                    break
                
                articles_urls.extend(articles)
                print(f"Trouvé {len(articles)} articles sur la page {page}")
                
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors du scraping de la page {page}: {e}")
                break
        
        return articles_urls
    
    def _extract_articles_from_page(self, soup):
        """
        Extrait les URLs des articles depuis une page de liste
        """
        articles_data = []
        
        # cherche la zone principale contenant les articles
        main_tag = soup.find('main')
        if not main_tag:
            main_tag = soup.find('div', class_='content')
            
        if not main_tag:
            print("Zone principale non trouvée")
            return []
        
        # trouve tous les articles
        articles = main_tag.find_all('article')
        
        for article in articles:
            article_info = self._extract_article_preview(article)
            if article_info and article_info['url']:
                articles_data.append(article_info)
        
        return articles_data
    
    def _extract_article_preview(self, article):
        """
        Extrait les informations de base d'un article depuis sa preview
        """
        article_info = {
            'url': None,
            'title': None,
            'preview_image': None,
            'tag': None,
            'preview_date': None,
            'preview_summary': None
        }
        
        # extrait l'URL de l'article
        title_link = article.find('a', href=True)
        if not title_link:
            header = article.find('header')
            if header:
                title_link = header.find('a', href=True)
        
        if title_link:
            article_info['url'] = title_link['href']
            
            # extrait le titre depuis le lien
            h_tag = title_link.find(['h1', 'h2', 'h3', 'h4'])
            if h_tag:
                article_info['title'] = h_tag.get_text(strip=True)
        
        # extrait l'image de prévisualisation
        img_div = article.find('div', class_='post-thumbnail')
        if img_div:
            img_tag = img_div.find('img')
            if img_tag:
                article_info['preview_image'] = extract_image_info(img_tag)['url']
        
        # extrait le tag/catégorie
        tag_span = article.find('span', class_='favtag')
        if tag_span:
            article_info['tag'] = tag_span.get_text(strip=True)
        
        # extrait la date de preview
        date_span = article.find('span', class_='posted-on')
        if date_span:
            article_info['preview_date'] = date_span.get_text(strip=True)
        
        # extrait le résumé de preview
        excerpt_div = article.find('div', class_='entry-excerpt')
        if excerpt_div:
            article_info['preview_summary'] = excerpt_div.get_text(strip=True)
        
        return article_info
