import React from 'react';
import { formatDate, getTimeAgo, truncateText, capitalize } from '../utils/dateUtils';

export default function ArticleCard({ article, onClick }) {
  const handleImageError = (e) => {
    e.target.style.display = 'none';
  };

  return (
    <div 
      className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition-all duration-300 cursor-pointer transform hover:-translate-y-1 h-full flex flex-col"
      onClick={() => onClick(article)}
    >
      <div className="relative h-48 overflow-hidden">
        {article.thumbnail ? (
          <img 
            src={article.thumbnail} 
            alt={article.title}
            className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
            onError={handleImageError}
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
            <span className="text-5xl">📰</span>
          </div>
        )}
        <div className="absolute top-3 left-3 bg-blue-600 bg-opacity-90 text-white px-2 py-1 rounded-md text-xs font-semibold uppercase tracking-wide">
          {capitalize(article.category_scraped?.replace('-', ' ') || 'Article')}
        </div>
      </div>
      
      <div className="p-5 flex-1 flex flex-col">
        <h3 className="text-lg font-bold text-gray-900 mb-3 line-clamp-2 leading-tight">
          {truncateText(article.title, 80)}
        </h3>
        
        <div className="flex justify-between items-center text-sm text-gray-600 mb-3">
          <span className="font-medium">Par {article.author}</span>
          <span className="italic">{getTimeAgo(article.publication_date)}</span>
        </div>
        
        <p className="text-gray-700 text-sm line-clamp-3 mb-4 flex-1">
          {truncateText(article.summary || article.content, 120)}
        </p>
        
        <div className="flex justify-between items-center mt-auto">
          <div className="flex items-center gap-2">
            {article.images && article.images.length > 0 && (
              <span className="text-xs text-gray-500 flex items-center gap-1">
                📷 {article.images.length}
              </span>
            )}
          </div>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-md text-sm font-medium transition-colors duration-200">
            Lire l'article
          </button>
        </div>
      </div>
    </div>
  );
}
