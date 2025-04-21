import { defineStore } from 'pinia'
import { authApi } from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: !!localStorage.getItem('token'),
    loading: false,
    error: null
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated,
    hasError: (state) => state.error !== null
  },

  actions: {
    async login(email, password, remember = false) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authApi.login({
          username: email, // Netlify Functions использует username для логина
          password
        })

        const { access_token, refresh_token } = response.data

        this.token = access_token
        this.isAuthenticated = true

        // Сохраняем токены
        localStorage.setItem('token', access_token)
        if (refresh_token) {
          localStorage.setItem('refresh_token', refresh_token)
        }

        // Загружаем данные пользователя
        await this.fetchUserProfile()
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка при входе'
        throw error
      } finally {
        this.loading = false
      }
    },

    async logout() {
      this.token = null
      this.user = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
      localStorage.removeItem('refresh_token')
    },

    async fetchUserProfile() {
      if (!this.token) return

      try {
        const response = await authApi.getUser()
        this.user = response.data
        this.isAuthenticated = true
        return this.user
      } catch (error) {
        if (error.response?.status === 401) {
          // Токен недействителен, разлогиниваем пользователя
          this.logout()
        }
        throw error
      }
    },

    async checkAuth() {
      if (!this.token) return false

      try {
        await this.fetchUserProfile()
        return true
      } catch (error) {
        return false
      }
    },

    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authApi.signup(userData)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка при регистрации'
        throw error
      } finally {
        this.loading = false
      }
    },

    async forgotPassword(email) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authApi.forgotPassword(email)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка при запросе сброса пароля'
        throw error
      } finally {
        this.loading = false
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