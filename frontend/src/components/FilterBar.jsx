import React from 'react';
import { capitalize } from '../utils/dateUtils';

export default function FilterBar({ 
  categories, 
  selectedCategory, 
  onCategoryChange,
  sortBy,
  onSortChange,
  stats
}) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm mb-8">
      <div className="flex flex-wrap gap-6 items-center mb-6">
        <div className="flex items-center gap-3">
          <label className="text-sm font-semibold text-gray-700">Catégorie :</label>
          <select 
            value={selectedCategory} 
            onChange={(e) => onCategoryChange(e.target.value)}
            className="px-3 py-2 border-2 border-gray-200 rounded-lg text-sm bg-white text-gray-700 cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          >
            <option value="all">Toutes les catégories</option>
            {categories.map(category => (
              <option key={category} value={category}>
                {capitalize(category.replace('-', ' '))} ({stats.byCategory[category]})
              </option>
            ))}
          </select>
        </div>

        <div className="flex items-center gap-3">
          <label className="text-sm font-semibold text-gray-700">Trier par :</label>
          <select 
            value={sortBy} 
            onChange={(e) => onSortChange(e.target.value)}
            className="px-3 py-2 border-2 border-gray-200 rounded-lg text-sm bg-white text-gray-700 cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          >
            <option value="date">Date de publication</option>
            <option value="title">Titre (A-Z)</option>
            <option value="author">Auteur (A-Z)</option>
          </select>
        </div>
      </div>

      <div className="flex flex-wrap gap-8 pt-4 border-t border-gray-100">
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">{stats.total}</div>
          <div className="text-sm text-gray-500">articles</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">{categories.length}</div>
          <div className="text-sm text-gray-500">catégories</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">{stats.authors}</div>
          <div className="text-sm text-gray-500">auteurs</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">{stats.withImages}</div>
          <div className="text-sm text-gray-500">avec images</div>
        </div>
      </div>
    </div>
  );
}
