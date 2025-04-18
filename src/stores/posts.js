import { defineStore } from 'pinia'
import axios from 'axios'

export const usePostsStore = defineStore('posts', {
  state: () => ({
    posts: [],
    currentPost: null,
    loading: false,
    error: null,
    filters: {
      channelId: null,
      status: 'all',
      dateRange: 'all',
      searchQuery: ''
    },
    pagination: {
      page: 1,
      perPage: 20,
      total: 0
    }
  }),

  getters: {
    getPostById: (state) => (id) => state.posts.find(post => post.id === id),
    filteredPosts: (state) => {
      let filtered = [...state.posts]

      if (state.filters.channelId) {
        filtered = filtered.filter(post => post.channelId === state.filters.channelId)
      }

      if (state.filters.status !== 'all') {
        filtered = filtered.filter(post => post.status === state.filters.status)
      }

      if (state.filters.searchQuery) {
        const query = state.filters.searchQuery.toLowerCase()
        filtered = filtered.filter(post => 
          post.title.toLowerCase().includes(query) ||
          post.description.toLowerCase().includes(query) ||
          post.tags.some(tag => tag.toLowerCase().includes(query))
        )
      }

      return filtered
    }
  },

  actions: {
    async fetchPosts(params = {}) {
      this.loading = true
      try {
        const { channelId, page = 1, perPage = 20 } = params
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/posts`, {
          params: {
            channelId,
            page,
            perPage,
            ...this.filters
          }
        })
        
        this.posts = response.data.posts
        this.pagination = {
          page: response.data.page,
          perPage: response.data.perPage,
          total: response.data.total
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при загрузке постов'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchPostDetails(postId) {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/posts/${postId}`)
        this.currentPost = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при загрузке информации о посте'
        throw error
      }
    },

    async createPost(postData) {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/posts`, postData)
        this.posts.unshift(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при создании поста'
        throw error
      }
    },

    async updatePost(postId, postData) {
      try {
        const response = await axios.put(`${import.meta.env.VITE_API_URL}/posts/${postId}`, postData)
        const index = this.posts.findIndex(p => p.id === postId)
        if (index !== -1) {
          this.posts[index] = response.data
        }
        if (this.currentPost?.id === postId) {
          this.currentPost = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при обновлении поста'
        throw error
      }
    },

    async deletePost(postId) {
      try {
        await axios.delete(`${import.meta.env.VITE_API_URL}/posts/${postId}`)
        this.posts = this.posts.filter(p => p.id !== postId)
        if (this.currentPost?.id === postId) {
          this.currentPost = null
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при удалении поста'
        throw error
      }
    },

    async schedulePost(postId, scheduledAt) {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/posts/${postId}/schedule`, {
          scheduledAt
        })
        const index = this.posts.findIndex(p => p.id === postId)
        if (index !== -1) {
          this.posts[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка при планировании публикации'
        throw error
      }
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.page = 1 // Сброс пагинации при изменении фильтров
    },

    clearFilters() {
      this.filters = {
        channelId: null,
        status: 'all',
        dateRange: 'all',
        searchQuery: ''
      }
    }
  }
}) 