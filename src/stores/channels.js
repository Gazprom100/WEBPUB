import { defineStore } from 'pinia'
import axios from 'axios'

export const useChannelsStore = defineStore('channels', {
  state: () => ({
    channels: [],
    currentChannel: null,
    loading: false,
    error: null,
    stats: {
      totalSubscribers: 0,
      totalViews: 0,
      averageEngagement: 0,
      totalRevenue: 0
    }
  }),

  getters: {
    getChannelById: (state) => (id) => state.channels.find(channel => channel.id === id),
    hasChannels: (state) => state.channels.length > 0,
    sortedChannels: (state) => [...state.channels].sort((a, b) => b.subscribers - a.subscribers)
  },

  actions: {
    async fetchChannels() {
      this.loading = true
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/channels`)
        this.channels = response.data
        await this.updateChannelsStats()
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при загрузке каналов'
        throw error
      } finally {
        this.loading = false
      }
    },

    async addChannel(channelData) {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/channels`, channelData)
        this.channels.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при добавлении канала'
        throw error
      }
    },

    async updateChannel(channelId, channelData) {
      try {
        const response = await axios.put(`${import.meta.env.VITE_API_URL}/channels/${channelId}`, channelData)
        const index = this.channels.findIndex(c => c.id === channelId)
        if (index !== -1) {
          this.channels[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при обновлении канала'
        throw error
      }
    },

    async deleteChannel(channelId) {
      try {
        await axios.delete(`${import.meta.env.VITE_API_URL}/channels/${channelId}`)
        this.channels = this.channels.filter(c => c.id !== channelId)
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при удалении канала'
        throw error
      }
    },

    async fetchChannelDetails(channelId) {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/channels/${channelId}`)
        this.currentChannel = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при загрузке информации о канале'
        throw error
      }
    },

    async updateChannelsStats() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/channels/stats`)
        this.stats = response.data
      } catch (error) {
        console.error('Ошибка при обновлении статистики:', error)
      }
    },

    async connectChannel(platform, username) {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/channels/connect`, {
          platform,
          username
        })
        this.channels.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при подключении канала'
        throw error
      }
    }
  }
}) 