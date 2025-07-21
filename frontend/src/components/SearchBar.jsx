import React from 'react';

export default function SearchBar({ searchTerm, onSearchChange, articlesCount }) {
  return (
    <div className="mb-8">
      <div className="relative max-w-2xl mx-auto">
        <input
          type="text"
          placeholder="Rechercher dans les articles..."
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          className="w-full px-4 py-3 pr-12 text-gray-900 placeholder-gray-500 bg-white border-2 border-gray-200 rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
        />
        <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 text-lg pointer-events-none">
          🔍
        </span>
      </div>
      {searchTerm && (
        <div className="text-center mt-2 text-sm text-gray-600">
          {articlesCount} article{articlesCount > 1 ? 's' : ''} trouvé{articlesCount > 1 ? 's' : ''}
        </div>
      )}
    </div>
  );
}
