import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false,
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
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/auth/login`, {
          email,
          password
        })

        const { token, user } = response.data

        this.token = token
        this.user = user
        this.isAuthenticated = true

        if (remember) {
          localStorage.setItem('token', token)
        }

        // Устанавливаем токен для всех последующих запросов
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при входе'
        throw error
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        await axios.post(`${import.meta.env.VITE_API_URL}/auth/logout`)
      } catch (error) {
        console.error('Ошибка при выходе:', error)
      } finally {
        this.token = null
        this.user = null
        this.isAuthenticated = false
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
      }
    },

    async checkAuth() {
      if (!this.token) return

      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/auth/me`)
        this.user = response.data
        this.isAuthenticated = true
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      } catch (error) {
        this.token = null
        this.user = null
        this.isAuthenticated = false
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
      }
    },

    async updateProfile(userData) {
      try {
        const response = await axios.put(`${import.meta.env.VITE_API_URL}/auth/profile`, userData)
        this.user = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при обновлении профиля'
        throw error
      }
    }
  }
}) 