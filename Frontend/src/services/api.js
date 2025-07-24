const API_BASE_URL = 'http://localhost:5000';

const apiRequest = async (endpoint, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.erro || `Erro ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Erro na API (${endpoint}):`, error);
    throw error;
  }
};

export const roupasAPI = {
  getAll: () => apiRequest('/roupas'),

  create: (roupa) => apiRequest('/roupas', {
    method: 'POST',
    body: JSON.stringify(roupa),
  }),

  update: (id, roupa) => apiRequest(`/roupas/${id}`, {
    method: 'PUT',
    body: JSON.stringify(roupa),
  }),

  delete: (id) => apiRequest(`/roupas/${id}`, {
    method: 'DELETE',
  }),

  getImageUrl: (imagePath) => {
    if (!imagePath || imagePath.trim() === '') {
      return null;
    }
    return `${API_BASE_URL}/imagens/${imagePath}`;
  },

  uploadImage: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await fetch(`${API_BASE_URL}/upload-imagem`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.erro || 'Erro no upload');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Erro no upload:', error);
      throw error;
    }
  },
};

export default roupasAPI;
