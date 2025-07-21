import { useState } from "react";
import { useArticles } from "./hooks/useArticles";
import SearchBar from "./components/SearchBar";
import FilterBar from "./components/FilterBar";
import ArticleCard from "./components/ArticleCard";
import ArticleDetail from "./components/ArticleDetail";

export default function App() {
  const {
    articles,
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
  } = useArticles();

  const [selectedArticle, setSelectedArticle] = useState(null);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement des articles...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center max-w-md mx-auto p-8">
          <h2 className="text-2xl font-bold text-red-600 mb-4">❌ Erreur</h2>
          <p className="text-gray-700 mb-2">{error}</p>
          <p className="text-gray-500">
            Assurez-vous que le fichier articles.json est présent dans le
            dossier public.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white text-center py-12 shadow-lg">
        <h1 className="text-4xl md:text-5xl font-extrabold mb-2 drop-shadow-sm">
          📰 Blog Scrapper
        </h1>
        <p className="text-lg md:text-xl font-light opacity-90">
          Explorez les articles du Blog du Modérateur
        </p>
      </header>

      <main className="flex-1 max-w-7xl mx-auto px-4 py-8 w-full">
        <SearchBar
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
          articlesCount={articles.length}
        />

        <FilterBar
          categories={categories}
          selectedCategory={selectedCategory}
          onCategoryChange={setSelectedCategory}
          sortBy={sortBy}
          onSortChange={setSortBy}
          stats={stats}
        />

        {articles.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-xl shadow-sm mt-8">
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              Aucun article trouvé
            </h3>
            <p className="text-gray-500">
              Essayez de modifier vos critères de recherche ou de filtrage.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-8">
            {articles.map((article, index) => (
              <ArticleCard
                key={`${article.url}-${index}`}
                article={article}
                onClick={setSelectedArticle}
              />
            ))}
          </div>
        )}
      </main>

      {selectedArticle && (
        <ArticleDetail
          article={selectedArticle}
          onClose={() => setSelectedArticle(null)}
        />
      )}

      <footer className="bg-gray-800 text-white text-center py-6 mt-12">
        <p className="text-sm">
          Articles scrapés depuis le{" "}
          <a
            href="https://www.blogdumoderateur.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-400 hover:text-blue-300 font-semibold underline transition-colors"
          >
            Blog du Modérateur
          </a>
        </p>
      </footer>
    </div>
  );
}
