<template>
  <div class="channels-list">
    <div class="list-header">
      <h2>Your Channels</h2>
      <button class="btn-add" @click="$router.push('/channels/new')">
        Add Channel
      </button>
    </div>

    <div class="channels-grid">
      <div v-for="channel in channels" :key="channel.id" class="channel-card">
        <div class="channel-image">
          <img :src="channel.avatar || '/default-channel.png'" :alt="channel.name">
          <span class="subscribers">{{ formatNumber(channel.subscribersCount) }} subscribers</span>
        </div>
        <div class="channel-info">
          <h3>{{ channel.name }}</h3>
          <p class="description">{{ channel.description }}</p>
          <div class="stats">
            <div class="stat">
              <span class="label">Posts</span>
              <span class="value">{{ channel.postsCount }}</span>
            </div>
            <div class="stat">
              <span class="label">Views</span>
              <span class="value">{{ formatNumber(channel.viewsCount) }}</span>
            </div>
            <div class="stat">
              <span class="label">Engagement</span>
              <span class="value">{{ formatPercent(channel.engagementRate) }}%</span>
            </div>
          </div>
        </div>
        <div class="channel-actions">
          <router-link :to="'/channels/' + channel.id" class="btn-view">View Details</router-link>
          <button class="btn-menu" @click="showChannelMenu(channel)">⋮</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">
      Loading channels...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else-if="channels.length === 0" class="empty">
      You don't have any channels yet. Add your first channel to get started!
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const channels = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/channels`)
    channels.value = response.data
  } catch (err) {
    error.value = 'Failed to load channels'
    console.error(err)
  } finally {
    loading.value = false
  }
})

const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const formatPercent = (num) => {
  return (num * 100).toFixed(1)
}

const showChannelMenu = (channel) => {
  // Show channel menu with options (edit, delete, etc.)
}
</script>

<style scoped>
.channels-list {
  padding: 2rem;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.btn-add {
  padding: 0.5rem 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: opacity 0.2s;
}

.btn-add:hover {
  opacity: 0.9;
}

.channels-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.channel-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.channel-card:hover {
  transform: translateY(-2px);
}

.channel-image {
  position: relative;
  height: 160px;
}

.channel-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.subscribers {
  position: absolute;
  bottom: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.25rem 0.5rem;
  font-size: 0.9rem;
}

.channel-info {
  padding: 1rem;
}

h3 {
  margin: 0 0 0.5rem;
  color: var(--text-color);
}

.description {
  color: var(--text-color);
  opacity: 0.8;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat .label {
  font-size: 0.8rem;
  color: var(--text-color);
  opacity: 0.8;
}

.stat .value {
  font-weight: bold;
  color: var(--secondary-color);
}

.channel-actions {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  background: #f8f8f8;
}

.btn-view {
  text-decoration: none;
  color: var(--primary-color);
  font-weight: 500;
}

.btn-menu {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: var(--text-color);
  opacity: 0.6;
  transition: opacity 0.2s;
}

.btn-menu:hover {
  opacity: 1;
}

.loading, .error, .empty {
  text-align: center;
  padding: 2rem;
  color: var(--text-color);
}

.error {
  color: #dc3545;
}
</style> 