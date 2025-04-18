import { defineStore } from 'pinia'
import axios from 'axios'

export const useNotificationsStore = defineStore('notifications', {
  state: () => ({
    notifications: [],
    unreadCount: 0,
    loading: false,
    error: null,
    pagination: {
      page: 1,
      perPage: 10,
      total: 0,
      hasMore: false
    }
  }),

  getters: {
    hasUnread: (state) => state.unreadCount > 0,
    hasMore: (state) => state.pagination.hasMore
  },

  actions: {
    async fetchNotifications(page = 1) {
      this.loading = true
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/notifications`, {
          params: {
            page,
            perPage: this.pagination.perPage
          }
        })

        if (page === 1) {
          this.notifications = response.data.notifications
        } else {
          this.notifications.push(...response.data.notifications)
        }

        this.pagination = {
          page: response.data.page,
          perPage: response.data.perPage,
          total: response.data.total,
          hasMore: response.data.hasMore
        }

        this.unreadCount = response.data.unreadCount
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при загрузке уведомлений'
        throw error
      } finally {
        this.loading = false
      }
    },

    async markAsRead(notificationId) {
      try {
        await axios.post(`${import.meta.env.VITE_API_URL}/notifications/${notificationId}/read`)
        
        const notification = this.notifications.find(n => n.id === notificationId)
        if (notification && !notification.read) {
          notification.read = true
          this.unreadCount--
        }
      } catch (error) {
        console.error('Ошибка при отметке уведомления как прочитанного:', error)
      }
    },

    async markAllAsRead() {
      try {
        await axios.post(`${import.meta.env.VITE_API_URL}/notifications/mark-all-read`)
        
        this.notifications.forEach(notification => {
          notification.read = true
        })
        this.unreadCount = 0
      } catch (error) {
        console.error('Ошибка при отметке всех уведомлений как прочитанных:', error)
      }
    },

    async loadMore() {
      if (this.hasMore && !this.loading) {
        await this.fetchNotifications(this.pagination.page + 1)
      }
    },

    // Добавление нового уведомления (например, через WebSocket)
    addNotification(notification) {
      this.notifications.unshift(notification)
      if (!notification.read) {
        this.unreadCount++
      }
    },

    // Очистка уведомлений
    clearNotifications() {
      this.notifications = []
      this.unreadCount = 0
      this.pagination = {
        page: 1,
        perPage: 10,
        total: 0,
        hasMore: false
      }
    },

    // Инициализация WebSocket подключения для real-time уведомлений
    initializeWebSocket() {
      const ws = new WebSocket(`${import.meta.env.VITE_WS_URL}/notifications`)

      ws.onmessage = (event) => {
        const notification = JSON.parse(event.data)
        this.addNotification(notification)
      }

      ws.onclose = () => {
        // Переподключение через 5 секунд
        setTimeout(() => this.initializeWebSocket(), 5000)
      }
    }
  }
}) 