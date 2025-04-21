<template>
  <div class="channels-view">
    <div class="header">
      <h1>Ваши каналы</h1>
      <button class="btn-add" @click="navigateToAddChannel">
        <i class="fas fa-plus"></i> Подключить новый канал
      </button>
    </div>

    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Загрузка каналов...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchChannels" class="btn-retry">Попробовать снова</button>
    </div>

    <div v-else-if="channels.length === 0" class="empty-state">
      <div class="empty-icon">📺</div>
      <h3>У вас пока нет подключенных каналов</h3>
      <p>Подключите свой первый канал, чтобы начать работу с контентом</p>
      <button @click="navigateToAddChannel" class="btn-primary">Подключить канал</button>
    </div>

    <div v-else class="channels-grid">
      <div v-for="channel in channels" :key="channel.id" class="channel-card">
        <div class="channel-avatar">
          <img v-if="channel.avatar_url" :src="channel.avatar_url" :alt="channel.name">
          <div v-else class="avatar-placeholder">{{ getChannelInitials(channel.name) }}</div>
        </div>

        <div class="channel-info">
          <h3 class="channel-name">{{ channel.name }}</h3>
          <div class="channel-stats">
            <div class="stat">
              <i class="fas fa-users"></i>
              <span>{{ formatNumber(channel.subscribers_count) }}</span>
            </div>
            <div class="stat">
              <i class="fas fa-eye"></i>
              <span>{{ formatNumber(channel.views_count) }}</span>
            </div>
          </div>
          <div class="channel-category">{{ channel.category }}</div>
        </div>

        <div class="channel-actions">
          <button @click="viewChannelFeed(channel.id)" class="btn-view-feed">
            <i class="fas fa-calendar-alt"></i> Лента новостей
          </button>
          <button @click="viewChannelAnalytics(channel.id)" class="btn-analytics">
            <i class="fas fa-chart-bar"></i> Аналитика
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const channels = ref([])
const isLoading = ref(true)
const error = ref(null)

onMounted(() => {
  fetchChannels()
})

const fetchChannels = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    // В реальном приложении замените на фактический API endpoint
    const response = await axios.get('/api/channels')
    channels.value = response.data
  } catch (err) {
    console.error('Ошибка при загрузке каналов:', err)
    error.value = 'Не удалось загрузить каналы. Пожалуйста, попробуйте позже.'
  } finally {
    isLoading.value = false
  }
}

const navigateToAddChannel = () => {
  router.push('/add-channel')
}

const viewChannelFeed = (channelId) => {
  router.push(`/channels/${channelId}/feed`)
}

const viewChannelAnalytics = (channelId) => {
  router.push(`/channels/${channelId}/analytics`)
}

const getChannelInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(word => word[0]?.toUpperCase() || '').join('').substring(0, 2)
}

const formatNumber = (num) => {
  if (num === undefined || num === null) return '0'
  
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}
</script>

<style scoped>
.channels-view {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h1 {
  font-size: 2rem;
  color: #1a1a1a;
  margin: 0;
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #4299E1;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-add:hover {
  background-color: #3182CE;
}

.loading-container, .error-container, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  text-align: center;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #4299E1;
  width: 40px;
  height: 40px;
  margin-bottom: 1rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #1a1a1a;
}

.empty-state p {
  color: #666;
  margin-bottom: 1.5rem;
  max-width: 400px;
}

.btn-primary, .btn-retry {
  background-color: #4299E1;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover, .btn-retry:hover {
  background-color: #3182CE;
}

.channels-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.channel-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s, box-shadow 0.2s;
}

.channel-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05), 0 4px 6px rgba(0, 0, 0, 0.08);
}

.channel-avatar {
  margin-bottom: 1rem;
  align-self: center;
}

.channel-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #4299E1;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: bold;
}

.channel-info {
  flex: 1;
  margin-bottom: 1rem;
}

.channel-name {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0 0 0.5rem;
  text-align: center;
  color: #1a1a1a;
}

.channel-stats {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 0.5rem;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #666;
  font-size: 0.9rem;
}

.channel-category {
  text-align: center;
  font-size: 0.9rem;
  color: #718096;
  background-color: #EDF2F7;
  border-radius: 9999px;
  padding: 0.25rem 0.75rem;
  display: inline-block;
  margin: 0 auto;
}

.channel-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.btn-view-feed, .btn-analytics {
  padding: 0.6rem 1rem;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-view-feed {
  background-color: #4299E1;
  color: white;
  border: none;
}

.btn-view-feed:hover {
  background-color: #3182CE;
}

.btn-analytics {
  background-color: transparent;
  border: 1px solid #CBD5E0;
  color: #4A5568;
}

.btn-analytics:hover {
  background-color: #F7FAFC;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .channels-grid {
    grid-template-columns: 1fr;
  }
}
</style> 