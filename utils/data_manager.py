import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class DataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.articles_file = os.path.join(data_dir, "articles.json")
        # Chemin pour le frontend React
        self.frontend_dir = "frontend/public"
        self.frontend_articles_file = os.path.join(self.frontend_dir, "articles.json")
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Crée les dossiers data et frontend/public s'ils n'existent pas"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Créer le dossier frontend/public s'il n'existe pas
        if not os.path.exists(self.frontend_dir):
            os.makedirs(self.frontend_dir)
    
    def save_articles(self, articles: List[Dict]):
        """
        Sauvegarde une liste d'articles dans le fichier JSON
        """
        # Charger les articles existants
        existing_articles = self.load_articles()
        
        # Créer un dictionnaire pour éviter les doublons (basé sur l'URL)
        articles_dict = {article['url']: article for article in existing_articles}
        
        # Ajouter les nouveaux articles
        new_count = 0
        for article in articles:
            if article['url'] not in articles_dict:
                # Ajouter timestamp de sauvegarde
                article['scraped_at'] = datetime.now().isoformat()
                articles_dict[article['url']] = article
                new_count += 1
            else:
                # Mettre à jour l'article existant si nécessaire
                articles_dict[article['url']].update(article)
                articles_dict[article['url']]['updated_at'] = datetime.now().isoformat()
        
        # Convertir en liste et sauvegarder
        all_articles = list(articles_dict.values())
        
        # Sauvegarder dans le dossier data principal
        with open(self.articles_file, 'w', encoding='utf-8') as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=2)
        
        # Sauvegarder aussi dans frontend/public pour React
        try:
            with open(self.frontend_articles_file, 'w', encoding='utf-8') as f:
                json.dump(all_articles, f, ensure_ascii=False, indent=2)
            print(f"Articles également sauvegardés pour le frontend: {self.frontend_articles_file}")
        except Exception as e:
            print(f"Attention: impossible de sauvegarder dans frontend/public: {e}")
        
        print(f"Sauvegarde terminée. {new_count} nouveaux articles ajoutés.")
        print(f"Total d'articles dans la base: {len(all_articles)}")
        
        return len(all_articles)
    
    def load_articles(self) -> List[Dict]:
        """
        Charge tous les articles depuis le fichier JSON
        """
        if not os.path.exists(self.articles_file):
            return []
        
        try:
            with open(self.articles_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print("Erreur lors du chargement des articles existants")
            return []
    
    def search_articles(self, 
                       category: Optional[str] = None,
                       subcategory: Optional[str] = None,
                       author: Optional[str] = None,
                       date_start: Optional[str] = None,
                       date_end: Optional[str] = None,
                       title_search: Optional[str] = None) -> List[Dict]:
        """
        Recherche des articles selon différents critères
        """
        articles = self.load_articles()
        filtered_articles = []
        
        for article in articles:
            # Filtre par catégorie
            if category and article.get('category'):
                if category.lower() not in article['category'].lower():
                    continue
            
            # Filtre par sous-catégorie
            if subcategory and article.get('subcategory'):
                if subcategory.lower() not in article['subcategory'].lower():
                    continue
            
            # Filtre par auteur
            if author and article.get('author'):
                if author.lower() not in article['author'].lower():
                    continue
            
            # Filtre par date de début
            if date_start and article.get('publication_date'):
                if article['publication_date'] < date_start:
                    continue
            
            # Filtre par date de fin
            if date_end and article.get('publication_date'):
                if article['publication_date'] > date_end:
                    continue
            
            # Recherche dans le titre
            if title_search and article.get('title'):
                if title_search.lower() not in article['title'].lower():
                    continue
            
            filtered_articles.append(article)
        
        return filtered_articles
    
    def get_categories(self) -> List[str]:
        """
        Retourne la liste des catégories disponibles
        """
        articles = self.load_articles()
        categories = set()
        
        for article in articles:
            if article.get('category'):
                categories.add(article['category'])
        
        return sorted(list(categories))
    
    def get_subcategories(self, category: Optional[str] = None) -> List[str]:
        """
        Retourne la liste des sous-catégories disponibles
        """
        articles = self.load_articles()
        subcategories = set()
        
        for article in articles:
            # Filtrer par catégorie si spécifiée
            if category and article.get('category'):
                if category.lower() not in article['category'].lower():
                    continue
            
            if article.get('subcategory'):
                subcategories.add(article['subcategory'])
        
        return sorted(list(subcategories))
    
    def get_authors(self) -> List[str]:
        """
        Retourne la liste des auteurs disponibles
        """
        articles = self.load_articles()
        authors = set()
        
        for article in articles:
            if article.get('author'):
                authors.add(article['author'])
        
        return sorted(list(authors))
    
    def get_stats(self) -> Dict:
        """
        Retourne des statistiques sur les articles
        """
        articles = self.load_articles()
        
        stats = {
            'total_articles': len(articles),
            'categories_count': len(self.get_categories()),
            'authors_count': len(self.get_authors()),
            'articles_with_images': sum(1 for a in articles if a.get('images')),
            'articles_with_content': sum(1 for a in articles if a.get('content')),
        }
        
        # Statistiques par catégorie
        category_stats = {}
        for article in articles:
            cat = article.get('category', 'Sans catégorie')
            category_stats[cat] = category_stats.get(cat, 0) + 1
        
        stats['by_category'] = category_stats
        
        return stats
    
    def export_to_csv(self, filename: Optional[str] = None):
        """
        Exporte les articles vers un fichier CSV
        """
        import csv
        
        if not filename:
            filename = os.path.join(self.data_dir, "articles_export.csv")
        
        articles = self.load_articles()
        
        if not articles:
            print("Aucun article à exporter")
            return
        
        # Définir les colonnes
        columns = [
            'url', 'title', 'category', 'subcategory', 'author', 
            'publication_date', 'summary', 'content', 'thumbnail',
            'images_count', 'scraped_at'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            
            for article in articles:
                row = {
                    'url': article.get('url', ''),
                    'title': article.get('title', ''),
                    'category': article.get('category', ''),
                    'subcategory': article.get('subcategory', ''),
                    'author': article.get('author', ''),
                    'publication_date': article.get('publication_date', ''),
                    'summary': article.get('summary', ''),
                    'content': article.get('content', ''),
                    'thumbnail': article.get('thumbnail', ''),
                    'images_count': len(article.get('images', [])),
                    'scraped_at': article.get('scraped_at', '')
                }
                writer.writerow(row)
        
        print(f"Export terminé: {filename}")
        print(f"{len(articles)} articles exportés")
