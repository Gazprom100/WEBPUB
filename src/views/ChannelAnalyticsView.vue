<template>
  <div class="channel-analytics-view">
    <div class="analytics-header">
      <div class="analytics-title">
        <h1>Аналитика канала "{{ channelName }}"</h1>
        <div class="channel-info" v-if="channel">
          <div class="info-item">
            <i class="fas fa-users"></i>
            <span>{{ formatNumber(channel.subscribers_count) }} подписчиков</span>
          </div>
          <div class="info-item">
            <i class="fas fa-eye"></i>
            <span>{{ formatNumber(channel.views_count) }} просмотров</span>
          </div>
        </div>
      </div>
      
      <div class="filter-controls">
        <div class="date-range-selector">
          <label for="dateRange">Период:</label>
          <select id="dateRange" v-model="selectedRange" class="select-control">
            <option v-for="(range, key) in dateRanges" :key="key" :value="key">
              {{ range.label }}
            </option>
          </select>
        </div>
        
        <button class="btn-export" @click="exportAnalytics">
          <i class="fas fa-file-export"></i> Экспорт
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Загрузка аналитики...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchChannelAnalytics" class="btn-retry">Попробовать снова</button>
    </div>

    <div v-else class="analytics-content">
      <!-- Общая статистика -->
      <div class="metrics-cards">
        <div class="metric-card">
          <div class="metric-title">Подписчики</div>
          <div class="metric-value">{{ formatNumber(analytics.subscribers_count) }}</div>
          <div :class="['metric-change', getChangeClass(analytics.subscribers_growth)]">
            <i :class="getChangeIconClass(analytics.subscribers_growth)"></i>
            {{ formatChange(analytics.subscribers_growth) }}%
          </div>
        </div>
        
        <div class="metric-card">
          <div class="metric-title">Просмотры</div>
          <div class="metric-value">{{ formatNumber(analytics.views_count) }}</div>
          <div :class="['metric-change', getChangeClass(analytics.views_growth)]">
            <i :class="getChangeIconClass(analytics.views_growth)"></i>
            {{ formatChange(analytics.views_growth) }}%
          </div>
        </div>
        
        <div class="metric-card">
          <div class="metric-title">Взаимодействие</div>
          <div class="metric-value">{{ formatPercent(analytics.engagement_rate) }}</div>
          <div :class="['metric-change', getChangeClass(analytics.engagement_growth)]">
            <i :class="getChangeIconClass(analytics.engagement_growth)"></i>
            {{ formatChange(analytics.engagement_growth) }}%
          </div>
        </div>
        
        <div class="metric-card">
          <div class="metric-title">Доход</div>
          <div class="metric-value">₽{{ formatNumber(analytics.revenue) }}</div>
          <div :class="['metric-change', getChangeClass(analytics.revenue_growth)]">
            <i :class="getChangeIconClass(analytics.revenue_growth)"></i>
            {{ formatChange(analytics.revenue_growth) }}%
          </div>
        </div>
      </div>

      <!-- Графики -->
      <div class="analytics-charts">
        <div class="chart-container">
          <h3>Динамика роста</h3>
          <div class="chart-placeholder">
            <p>Здесь будет график динамики подписчиков и просмотров</p>
          </div>
        </div>
        
        <div class="chart-container">
          <h3>Активность по дням</h3>
          <div class="chart-placeholder">
            <p>Здесь будет график активности по дням недели</p>
          </div>
        </div>
      </div>

      <!-- Лучшие публикации -->
      <div class="top-posts-section">
        <h3>Лучшие публикации</h3>
        <div class="posts-table">
          <table>
            <thead>
              <tr>
                <th>Публикация</th>
                <th>Дата</th>
                <th>Просмотры</th>
                <th>Взаимодействие</th>
                <th>CTR</th>
                <th>Доход</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(post, index) in analytics.top_posts" :key="index">
                <td class="post-title">
                  <div class="post-info">
                    <div v-if="post.image_url" class="post-image">
                      <img :src="post.image_url" :alt="post.title">
                    </div>
                    <div v-else class="post-image placeholder-image">
                      <i class="fas fa-file-image"></i>
                    </div>
                    <div>
                      <div class="title">{{ post.title }}</div>
                      <div class="category">{{ post.category }}</div>
                    </div>
                  </div>
                </td>
                <td>{{ formatDate(post.published_at) }}</td>
                <td>{{ formatNumber(post.views) }}</td>
                <td>{{ formatPercent(post.engagement_rate) }}</td>
                <td>{{ formatPercent(post.ctr) }}</td>
                <td>₽{{ formatNumber(post.revenue) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Демография аудитории -->
      <div class="audience-section">
        <h3>Аудитория</h3>
        <div class="audience-charts">
          <div class="audience-chart">
            <h4>По возрасту</h4>
            <div class="chart-placeholder">
              <p>Здесь будет график возрастного распределения</p>
            </div>
          </div>
          <div class="audience-chart">
            <h4>По местоположению</h4>
            <div class="chart-placeholder">
              <p>Здесь будет график географического распределения</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const channelId = computed(() => route.params.id)

const channel = ref(null)
const channelName = ref('...')
const analytics = ref({
  subscribers_count: 0,
  subscribers_growth: 0,
  views_count: 0,
  views_growth: 0,
  engagement_rate: 0,
  engagement_growth: 0,
  revenue: 0,
  revenue_growth: 0,
  top_posts: []
})
const isLoading = ref(true)
const error = ref(null)

const dateRanges = {
  '7d': { label: 'Последние 7 дней', days: 7 },
  '30d': { label: 'Последние 30 дней', days: 30 },
  '90d': { label: 'Последние 90 дней', days: 90 },
  'ytd': { label: 'С начала года', days: null },
  'all': { label: 'Все время', days: null }
}

const selectedRange = ref('30d')

onMounted(() => {
  fetchChannelInfo()
  fetchChannelAnalytics()
})

const fetchChannelInfo = async () => {
  try {
    // В реальном приложении заменить на фактический API endpoint
    // const response = await axios.get(`/api/channels/${channelId.value}`)
    // channel.value = response.data
    // channelName.value = channel.value.name

    // Временная заглушка
    channel.value = {
      id: channelId.value,
      name: 'Spacebot',
      subscribers_count: 125000,
      views_count: 3450000,
    }
    channelName.value = channel.value.name
  } catch (err) {
    console.error('Ошибка при загрузке информации о канале:', err)
    error.value = 'Не удалось загрузить информацию о канале.'
  }
}

const fetchChannelAnalytics = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    // В реальном приложении заменить на фактический API endpoint
    // const response = await axios.get(`/api/channels/${channelId.value}/analytics`, {
    //   params: { range: selectedRange.value }
    // })
    // analytics.value = response.data
    
    // Временная заглушка с демонстрационными данными
    setTimeout(() => {
      analytics.value = {
        subscribers_count: 125000,
        subscribers_growth: 5.2,
        views_count: 1450000,
        views_growth: 12.8,
        engagement_rate: 4.3,
        engagement_growth: -0.5,
        revenue: 28500,
        revenue_growth: 8.1,
        top_posts: [
          {
            id: 1,
            title: 'Как достичь звания Консультант за 30 дней',
            category: 'Обучение',
            image_url: null,
            published_at: '2023-10-15T10:00:00Z',
            views: 24500,
            engagement_rate: 8.9,
            ctr: 2.4,
            revenue: 4500
          },
          {
            id: 2,
            title: 'Поздравляем всех с Международным женским днем!',
            category: 'Праздник',
            image_url: null,
            published_at: '2023-03-08T09:30:00Z',
            views: 35200,
            engagement_rate: 12.5,
            ctr: 3.1,
            revenue: 5800
          },
          {
            id: 3,
            title: 'Релокация офиса: что нужно знать',
            category: 'Новости',
            image_url: null,
            published_at: '2023-09-25T14:15:00Z',
            views: 18600,
            engagement_rate: 6.2,
            ctr: 1.8,
            revenue: 2200
          },
          {
            id: 4,
            title: 'Новая коллекция осень-зима: предзаказ открыт',
            category: 'Продукты',
            image_url: null,
            published_at: '2023-08-12T12:00:00Z',
            views: 42800,
            engagement_rate: 9.7,
            ctr: 4.2,
            revenue: 8900
          },
          {
            id: 5,
            title: 'Еженедельная процедура по уходу за кожей',
            category: 'Советы',
            image_url: null,
            published_at: '2023-11-05T16:45:00Z',
            views: 22300,
            engagement_rate: 7.5,
            ctr: 2.8,
            revenue: 3900
          }
        ]
      }
      isLoading.value = false
    }, 800)
  } catch (err) {
    console.error('Ошибка при загрузке аналитики канала:', err)
    error.value = 'Не удалось загрузить аналитику канала.'
    isLoading.value = false
  }
}

const getChangeClass = (value) => {
  if (value > 0) return 'positive'
  if (value < 0) return 'negative'
  return 'neutral'
}

const getChangeIconClass = (value) => {
  if (value > 0) return 'fas fa-arrow-up'
  if (value < 0) return 'fas fa-arrow-down'
  return 'fas fa-minus'
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

const formatPercent = (num) => {
  if (num === undefined || num === null) return '0%'
  return num.toFixed(1) + '%'
}

const formatChange = (num) => {
  if (num === undefined || num === null) return '0'
  return Math.abs(num).toFixed(1)
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', { 
    day: '2-digit', 
    month: '2-digit', 
    year: '2-digit' 
  })
}

const exportAnalytics = () => {
  // Здесь должен быть код для экспорта аналитики
  alert('Экспорт аналитики канала')
}
</script>

<style scoped>
.channel-analytics-view {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.analytics-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.analytics-title h1 {
  font-size: 1.75rem;
  margin: 0 0 0.5rem;
  color: #1a1a1a;
}

.channel-info {
  display: flex;
  gap: 1rem;
  color: #4a5568;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.filter-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.date-range-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.select-control {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background-color: white;
  font-size: 0.9rem;
}

.btn-export {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  background-color: transparent;
  border: 1px solid #CBD5E0;
  color: #4A5568;
  transition: all 0.2s;
}

.btn-export:hover {
  background-color: #F7FAFC;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
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

.btn-retry {
  background-color: #4299E1;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.65rem 1.25rem;
  font-weight: 500;
  cursor: pointer;
  margin-top: 1rem;
}

.analytics-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.metrics-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
}

.metric-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.metric-title {
  color: #64748b;
  font-size: 0.9rem;
}

.metric-value {
  font-size: 1.8rem;
  font-weight: 600;
  color: #1e293b;
}

.metric-change {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
  font-weight: 500;
}

.metric-change.positive {
  color: #10b981;
}

.metric-change.negative {
  color: #ef4444;
}

.metric-change.neutral {
  color: #9ca3af;
}

.analytics-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
  gap: 1.5rem;
}

.chart-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  padding: 1.25rem;
}

.chart-container h3 {
  font-size: 1.25rem;
  margin: 0 0 1rem;
  color: #1e293b;
}

.chart-placeholder {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8fafc;
  border-radius: 8px;
  color: #64748b;
}

.top-posts-section {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  padding: 1.25rem;
}

.top-posts-section h3 {
  font-size: 1.25rem;
  margin: 0 0 1rem;
  color: #1e293b;
}

.posts-table {
  overflow-x: auto;
}

.posts-table table {
  width: 100%;
  border-collapse: collapse;
}

.posts-table th {
  text-align: left;
  padding: 0.75rem;
  color: #64748b;
  font-weight: 500;
  border-bottom: 1px solid #e2e8f0;
}

.posts-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
  color: #334155;
}

.post-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.post-image {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  overflow: hidden;
  background-color: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
}

.post-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-image {
  color: #94a3b8;
}

.post-title .title {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.post-title .category {
  font-size: 0.85rem;
  color: #64748b;
}

.audience-section {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  padding: 1.25rem;
}

.audience-section h3 {
  font-size: 1.25rem;
  margin: 0 0 1rem;
  color: #1e293b;
}

.audience-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.audience-chart h4 {
  font-size: 1rem;
  margin: 0 0 0.75rem;
  color: #334155;
}

@media (max-width: 768px) {
  .analytics-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .filter-controls {
    width: 100%;
    justify-content: space-between;
  }
  
  .analytics-charts,
  .audience-charts {
    grid-template-columns: 1fr;
  }
}
</style> 