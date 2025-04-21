import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: {
      id: '00000000-0000-0000-0000-000000000000',
      email: 'test@example.com',
      full_name: 'Test User',
      is_active: true,
      is_superuser: true
    },
    token: 'test-token',
    isAuthenticated: true
  }),

  actions: {
    async login(email, password) {
      // Пропускаем вход, сразу устанавливаем тестового пользователя
      this.user = {
        id: '00000000-0000-0000-0000-000000000000',
        email: 'test@example.com',
        full_name: 'Test User',
        is_active: true,
        is_superuser: true
      }
      this.token = 'test-token'
      this.isAuthenticated = true
      return true
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
    }
  }
}) 