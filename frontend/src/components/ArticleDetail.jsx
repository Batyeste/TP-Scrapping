import React from 'react';
import { formatDate, capitalize } from '../utils/dateUtils';

export default function ArticleDetail({ article, onClose }) {
  const handleImageError = (e) => {
    e.target.style.display = 'none';
  };

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  if (!article) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-start justify-center z-50 overflow-y-auto p-4" onClick={handleBackdropClick}>
      <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto my-auto">
        <div className="sticky top-0 bg-white p-4 border-b border-gray-200 flex justify-end z-10">
          <button 
            onClick={onClose}
            className="w-10 h-10 bg-gray-100 hover:bg-gray-200 border border-gray-300 rounded-full flex items-center justify-center text-xl transition-all hover:scale-110"
          >
            ✕
          </button>
        </div>

        <div className="pb-8">
          {article.thumbnail && (
            <div className="w-full max-h-80 overflow-hidden">
              <img 
                src={article.thumbnail} 
                alt={article.title}
                className="w-full h-full object-cover"
                onError={handleImageError}
              />
            </div>
          )}

          <div className="p-8">
            <div className="inline-block bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-semibold uppercase tracking-wide mb-4">
              {capitalize(article.category_scraped?.replace('-', ' ') || 'Article')}
            </div>

            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 leading-tight mb-6">{article.title}</h1>

            <div className="bg-gray-50 p-6 rounded-lg mb-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <strong className="text-gray-700">Auteur :</strong> <span className="text-gray-900">{article.author}</span>
                </div>
                <div>
                  <strong className="text-gray-700">Publié le :</strong> <span className="text-gray-900">{formatDate(article.publication_date)}</span>
                </div>
                <div>
                  <strong className="text-gray-700">Catégorie :</strong> <span className="text-gray-900">{article.category}</span>
                </div>
                {article.url && (
                  <div>
                    <a 
                      href={article.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 font-semibold hover:underline transition-colors"
                    >
                      📰 Voir l'article original
                    </a>
                  </div>
                )}
              </div>
            </div>

            {article.summary && (
              <div className="mb-8">
                <h3 className="text-xl font-bold text-gray-900 mb-4 pb-2 border-b-2 border-gray-200">Résumé</h3>
                <p className="text-lg text-gray-700 leading-relaxed italic bg-gray-50 p-4 rounded-lg">{article.summary}</p>
              </div>
            )}

            <div className="mb-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4 pb-2 border-b-2 border-gray-200">Contenu de l'article</h3>
              <div className="prose max-w-none">
                {article.content.split('\n').map((paragraph, index) => (
                  paragraph.trim() && (
                    <p key={index} className="text-gray-700 leading-relaxed mb-4 text-justify">{paragraph.trim()}</p>
                  )
                ))}
              </div>
            </div>

            {article.images && article.images.length > 0 && (
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-4 pb-2 border-b-2 border-gray-200">
                  Images de l'article ({article.images.length})
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
                  {article.images.map((image, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg overflow-hidden bg-gray-50">
                      <img 
                        src={image.url || image} 
                        alt={image.caption || `Image ${index + 1}`}
                        className="w-full h-48 object-cover"
                        onError={handleImageError}
                      />
                      {image.caption && (
                        <p className="p-4 text-sm text-gray-600 italic leading-relaxed">{image.caption}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
