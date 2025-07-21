import { useState, useEffect, useMemo } from 'react';

export const useArticles = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sortBy, setSortBy] = useState('date');

  //-- Charger les articles
  useEffect(() => {
    const loadArticles = async () => {
      try {
        setLoading(true);
        const response = await fetch('/articles.json');
        if (!response.ok) {
          throw new Error('Erreur lors du chargement des articles');
        }
        const data = await response.json();
        setArticles(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadArticles();
  }, []);

  //-- Filtrer et trier les articles
  const filteredArticles = useMemo(() => {
    let filtered = articles;

    //-- Filtrage par terme de recherche
    if (searchTerm) {
      filtered = filtered.filter(article =>
        article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        article.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
        article.author.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    //-- Filtrage par catégorie
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(article => 
        article.category_scraped === selectedCategory
      );
    }

    //-- Tri
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return b.publication_date.localeCompare(a.publication_date);
        case 'title':
          return a.title.localeCompare(b.title);
        case 'author':
          return a.author.localeCompare(b.author);
        default:
          return 0;
      }
    });

    return filtered;
  }, [articles, searchTerm, selectedCategory, sortBy]);

  //-- Obtenir les catégories uniques
  const categories = useMemo(() => {
    const uniqueCategories = [...new Set(articles.map(article => article.category_scraped))];
    return uniqueCategories.sort();
  }, [articles]);

  //-- Stats
  const stats = useMemo(() => {
    return {
      total: articles.length,
      byCategory: categories.reduce((acc, category) => {
        acc[category] = articles.filter(article => article.category_scraped === category).length;
        return acc;
      }, {}),
      authors: [...new Set(articles.map(article => article.author))].length,
      withImages: articles.filter(article => article.images && article.images.length > 0).length
    };
  }, [articles, categories]);

  return {
    articles: filteredArticles,
    loading,
    error,
    searchTerm,
    setSearchTerm,
    selectedCategory,
    setSelectedCategory,
    sortBy,
    setSortBy,
    categories,
    stats,
    totalArticles: articles.length
  };
};
