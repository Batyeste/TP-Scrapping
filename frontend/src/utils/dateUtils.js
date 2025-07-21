//-- formatage de la date
export const formatDate = (dateString) => {
  if (!dateString || dateString.length !== 8) {
    return 'Date inconnue';
  }

  const year = dateString.substring(0, 4);
  const month = dateString.substring(4, 6);
  const day = dateString.substring(6, 8);

  const months = [
    'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
    'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
  ];

  const monthIndex = parseInt(month) - 1;
  const monthName = months[monthIndex] || 'mois inconnu';

  return `${parseInt(day)} ${monthName} ${year}`;
};

export const getTimeAgo = (dateString) => {
  if (!dateString || dateString.length !== 8) {
    return 'Il y a longtemps';
  }

  const year = parseInt(dateString.substring(0, 4));
  const month = parseInt(dateString.substring(4, 6)) - 1; 
  const day = parseInt(dateString.substring(6, 8));

  const articleDate = new Date(year, month, day);
  const now = new Date();
  const diffTime = Math.abs(now - articleDate);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays === 1) {
    return 'Hier';
  } else if (diffDays === 0) {
    return 'Aujourd\'hui';
  } else if (diffDays < 7) {
    return `Il y a ${diffDays} jours`;
  } else if (diffDays < 30) {
    const weeks = Math.floor(diffDays / 7);
    return `Il y a ${weeks} semaine${weeks > 1 ? 's' : ''}`;
  } else if (diffDays < 365) {
    const months = Math.floor(diffDays / 30);
    return `Il y a ${months} mois`;
  } else {
    const years = Math.floor(diffDays / 365);
    return `Il y a ${years} an${years > 1 ? 's' : ''}`;
  }
};

export const truncateText = (text, maxLength = 150) => {
  if (!text || text.length <= maxLength) {
    return text;
  }
  return text.substring(0, maxLength).trim() + '...';
};

//-- Capitaliser la première lettre
export const capitalize = (str) => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
};
