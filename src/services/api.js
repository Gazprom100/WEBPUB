import axios from 'axios';

// Получаем базовый URL из переменной окружения
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Настраиваем базовый URL в зависимости от окружения
const baseURL = apiUrl.startsWith('http') 
  ? apiUrl 
  : `${window.location.origin}${apiUrl}`;

console.log('API BaseURL:', baseURL);

// Create axios instance with base URL
const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Для отладки
    console.log(`Sending ${config.method.toUpperCase()} request to: ${config.baseURL}${config.url}`);
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Auth endpoints
export const authApi = {
  signup: (userData) => api.post('/auth/signup', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  forgotPassword: (email) => api.post('/auth/forgot-password', { email }),
  resetPassword: (token, password) => api.post('/auth/reset-password', { token, password }),
  getUser: () => api.get('/auth/me'),
  // Тестовый эндпоинт для проверки соединения
  test: () => api.get('/test')
};

export default api; 