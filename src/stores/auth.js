import { defineStore } from 'pinia'
import { authApi } from '@/services/api'

// Тестовый пользователь для локального режима (без API)
const TEST_USER = {
  id: '12345',
  email: 'test@example.com',
  full_name: 'Test User',
  is_active: true
};

// Режим работы - используем локальную эмуляцию если API недоступен
let useLocalModeAfterFailure = false;

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: !!localStorage.getItem('token'),
    loading: false,
    error: null,
    isLocalMode: false
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated,
    hasError: (state) => state.error !== null
  },

  actions: {
    async login(email, password, remember = false) {
      this.loading = true;
      this.error = null;
      
      // Если API не работает, эмулируем вход локально
      if (useLocalModeAfterFailure) {
        return this.loginLocally(email, password);
      }
      
      try {
        // Пытаемся сделать запрос к API
        const response = await authApi.login({
          username: email,
          password
        });

        const { access_token, refresh_token } = response.data;

        this.token = access_token;
        this.isAuthenticated = true;

        localStorage.setItem('token', access_token);
        if (refresh_token) {
          localStorage.setItem('refresh_token', refresh_token);
        }

        // Загружаем данные пользователя
        await this.fetchUserProfile();
        
        // Запоминаем email если нужно
        if (remember) {
          localStorage.setItem('remember_email', email);
        }
        
        return { success: true };
      } catch (error) {
        // Если ошибка 404, значит API недоступен
        if (error.response?.status === 404) {
          console.warn('API недоступен, переключаемся в локальный режим');
          useLocalModeAfterFailure = true;
          return this.loginLocally(email, password);
        }
        
        this.error = error.response?.data?.detail || 'Ошибка при входе';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // Локальная эмуляция входа (без API)
    loginLocally(email, password) {
      console.log('Используем локальную аутентификацию');
      
      // Проверяем тестовые данные или любые данные в локальном режиме
      if (email === 'test@example.com' && password === 'password123') {
        this.isLocalMode = true;
        this.user = TEST_USER;
        this.isAuthenticated = true;
        
        // Симулируем токен
        const dummyToken = 'local-mode-token-123456';
        this.token = dummyToken;
        localStorage.setItem('token', dummyToken);
        
        return { success: true };
      } else if (this.isLocalMode) {
        // В локальном режиме пропускаем любые данные
        this.user = {
          id: Date.now().toString(),
          email,
          full_name: email.split('@')[0],
          is_active: true
        };
        this.isAuthenticated = true;
        
        const dummyToken = `local-mode-${Date.now()}`;
        this.token = dummyToken;
        localStorage.setItem('token', dummyToken);
        
        return { success: true };
      } else {
        this.error = 'Неверный email или пароль';
        throw new Error('Неверный email или пароль');
      }
    },

    async logout() {
      this.token = null;
      this.user = null;
      this.isAuthenticated = false;
      this.isLocalMode = false;
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
    },

    async fetchUserProfile() {
      if (!this.token) return;
      
      // Если в локальном режиме, просто возвращаем тестового пользователя
      if (this.isLocalMode) {
        this.user = TEST_USER;
        this.isAuthenticated = true;
        return this.user;
      }

      try {
        const response = await authApi.getUser();
        this.user = response.data;
        this.isAuthenticated = true;
        return this.user;
      } catch (error) {
        if (error.response?.status === 404) {
          // API недоступен, пробуем локальный режим
          console.warn('API недоступен при получении профиля, используем локальный режим');
          this.isLocalMode = true;
          this.user = TEST_USER;
          return this.user;
        } else if (error.response?.status === 401) {
          // Токен недействителен, разлогиниваем пользователя
          this.logout();
        }
        throw error;
      }
    },

    async checkAuth() {
      if (!this.token) return false;
      
      // Если в локальном режиме, просто подтверждаем аутентификацию
      if (this.isLocalMode) {
        this.user = TEST_USER;
        this.isAuthenticated = true;
        return true;
      }

      try {
        await this.fetchUserProfile();
        return true;
      } catch (error) {
        if (error.response?.status === 404) {
          // API недоступен, используем локальный режим
          this.isLocalMode = true;
          this.user = TEST_USER;
          this.isAuthenticated = true;
          return true;
        }
        return false;
      }
    },

    async register(userData) {
      this.loading = true;
      this.error = null;
      
      // Если API недоступен, эмулируем регистрацию
      if (useLocalModeAfterFailure) {
        this.isLocalMode = true;
        this.user = {
          id: Date.now().toString(),
          email: userData.email,
          full_name: userData.full_name,
          is_active: true
        };
        
        // Автоматический вход после регистрации
        return this.loginLocally(userData.email, userData.password);
      }
      
      try {
        const response = await authApi.signup(userData);
        return response.data;
      } catch (error) {
        if (error.response?.status === 404) {
          // API недоступен, переключаемся в локальный режим
          useLocalModeAfterFailure = true;
          this.isLocalMode = true;
          return this.register(userData);
        }
        
        this.error = error.response?.data?.detail || 'Ошибка при регистрации';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async forgotPassword(email) {
      this.loading = true;
      this.error = null;
      
      // Если в локальном режиме, эмулируем успешный сброс
      if (useLocalModeAfterFailure) {
        return { message: 'На ваш email отправлена инструкция по восстановлению пароля' };
      }
      
      try {
        const response = await authApi.forgotPassword(email);
        return response.data;
      } catch (error) {
        if (error.response?.status === 404) {
          // API недоступен
          useLocalModeAfterFailure = true;
          return { message: 'На ваш email отправлена инструкция по восстановлению пароля' };
        }
        
        this.error = error.response?.data?.detail || 'Ошибка при запросе сброса пароля';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateProfile(userData) {
      try {
        const response = await authApi.updateProfile(userData)
        this.user = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при обновлении профиля'
        throw error
      }
    }
  }
}) 