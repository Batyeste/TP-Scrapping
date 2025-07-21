import sys
import os
import time
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.list_scraper import ListScraper
from src.article_scraper import ArticleScraper
from utils.data_manager import DataManager


class BlogScrapingManager:
    def __init__(self):
        self.list_scraper = ListScraper()
        self.article_scraper = ArticleScraper()
        self.data_manager = DataManager()
        
        # URLs des différentes catégories du Blog du Modérateur
        self.categories_urls = {
            'web': 'https://www.blogdumoderateur.com/web/',
            'social-media': 'https://www.blogdumoderateur.com/social-media/',
            'mobile': 'https://www.blogdumoderateur.com/mobile/',
            'digital': 'https://www.blogdumoderateur.com/digital/',
            'e-commerce': 'https://www.blogdumoderateur.com/e-commerce/',
            'tech': 'https://www.blogdumoderateur.com/tech/',
        }
    
    def scrape_category(self, category_name: str, max_pages: int = 2, delay: float = 1.0):
        """
        Scrape une catégorie spécifique
        """
        if category_name not in self.categories_urls:
            print(f"Catégorie '{category_name}' non trouvée. Catégories disponibles: {list(self.categories_urls.keys())}")
            return
        
        url = self.categories_urls[category_name]
        print(f"Démarrage du scraping de la catégorie '{category_name}'")
        print(f"URL: {url}")
        print(f"Pages à scraper: {max_pages}")
        print("="*50)
        
        # Liste des articles
        print("récupération de la liste des articles...")
        articles_previews = self.list_scraper.fetch_articles_list(url, max_pages)
        
        if not articles_previews:
            print("Aucun article trouvé dans cette catégorie")
            return
        
        print(f"Trouvé {len(articles_previews)} articles à scraper")
        print("="*50)
        
        # Scrap le contenu complet de chaque article
        print("scraping du contenu complet des articles...")
        scraped_articles = []
        
        for i, preview in enumerate(articles_previews, 1):
            print(f"Scraping article {i}/{len(articles_previews)}: {preview.get('title', 'Sans titre')}")
            
            try:
                full_article = self.article_scraper.scrape_article_content(preview['url'])
                
                if full_article:
                    # fusionner les données complètes
                    full_article.update({
                        'category_scraped': category_name,  
                        'preview_data': preview  
                    })
                    scraped_articles.append(full_article)
                    print(f"  ✓ Article scraped avec succès")
                else:
                    print(f"  X Échec du scraping")
                
                # délai entre les requêtes
                if delay > 0:
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"  X Erreur lors du scraping: {e}")
                continue
        
        print("="*50)
        print(f"Scraping terminé. {len(scraped_articles)}/{len(articles_previews)} articles récupérés")
        
        # sauvegarde des données
        if scraped_articles:
            print("sauvegarde des données...")
            total_articles = self.data_manager.save_articles(scraped_articles)
            print(f"Articles sauvegardés. Total dans la base: {total_articles}")
        
        return scraped_articles
    
    def scrape_all_categories(self, max_pages_per_category: int = 1, delay: float = 1.0):
        """
        Scrape toutes les catégories
        """
        print("Démarrage du scraping de toutes les catégories")
        print(f"Catégories: {list(self.categories_urls.keys())}")
        print(f"Pages par catégorie: {max_pages_per_category}")
        print("="*60)
        
        all_articles = []
        
        for category_name in self.categories_urls.keys():
            print(f"\nDémarrage de la catégorie: {category_name}")
            articles = self.scrape_category(category_name, max_pages_per_category, delay)
            if articles:
                all_articles.extend(articles)
            
            # Pause entre les catégories
            if delay > 0:
                print(f"Pause de {delay * 2} secondes avant la prochaine catégorie...")
                time.sleep(delay * 2)
        
        print("="*60)
        print(f"Scraping global terminé. Total d'articles récupérés: {len(all_articles)}")
        
        return all_articles
    
    def show_stats(self):
        """
        Affiche les statistiques de la "base de données" : Json
        """
        stats = self.data_manager.get_stats()
        
        print("STATISTIQUES DE LA 'BASE DE DONNÉES'")
        print("="*40)
        print(f"Total d'articles: {stats['total_articles']}")
        print(f"Nombre de catégories: {stats['categories_count']}")
        print(f"Nombre d'auteurs: {stats['authors_count']}")
        print(f"Articles avec images: {stats['articles_with_images']}")
        print(f"Articles avec contenu: {stats['articles_with_content']}")
        
        print("\nRépartition par catégorie:")
        for category, count in stats['by_category'].items():
            print(f"  - {category}: {count} articles")


def main():
    """
    Fonction principale avec interface en ligne de commande
    """
    manager = BlogScrapingManager()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py <commande> [options]")
        print("\nCommandes disponibles:")
        print("  scrape <catégorie> [nombre de pages] - Scraper une catégorie spécifique")
        print("  scrape-all [nombre de pages]         - Scraper toutes les catégories")
        print("  stats                      - Afficher les statistiques")
        print("  export                     - Exporter vers CSV")
        print("\nCatégories disponibles:")
        for cat in manager.categories_urls.keys():
            print(f"  - {cat}")
        return
    
    command = sys.argv[1].lower()
    
    if command == "scrape":
        if len(sys.argv) < 3:
            print("Usage: python main.py scrape <catégorie> [pages]")
            return
        
        category = sys.argv[2]
        max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 2
        
        manager.scrape_category(category, max_pages)
    
    elif command == "scrape-all":
        max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        manager.scrape_all_categories(max_pages)
    
    elif command == "stats":
        manager.show_stats()
    
    elif command == "export":
        manager.data_manager.export_to_csv()
    
    else:
        print(f"Commande inconnue: {command}")


if __name__ == "__main__":
    main()
