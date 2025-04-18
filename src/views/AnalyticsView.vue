<template>
  <div class="analytics-view">
    <div class="analytics-header">
      <h1>Analytics Dashboard</h1>
      
      <div class="filters">
        <div class="channel-select">
          <select v-model="selectedChannel" class="form-input">
            <option value="">All Channels</option>
            <option v-for="channel in channels" :key="channel.id" :value="channel.id">
              {{ channel.name }}
            </option>
          </select>
        </div>

        <div class="date-range">
          <button 
            v-for="range in dateRanges" 
            :key="range.value"
            class="btn"
            :class="{ 'btn-primary': selectedRange === range.value }"
            @click="selectedRange = range.value"
          >
            {{ range.label }}
          </button>
        </div>
      </div>
    </div>

    <div class="analytics-grid">
      <!-- Overview Cards -->
      <div class="analytics-card">
        <h3>Total Subscribers</h3>
        <div class="metric">
          <span class="value">{{ formatNumber(metrics.totalSubscribers) }}</span>
          <span class="change" :class="{ 'positive': metrics.subscriberGrowth > 0 }">
            {{ formatPercent(metrics.subscriberGrowth) }}%
          </span>
        </div>
      </div>

      <div class="analytics-card">
        <h3>Total Views</h3>
        <div class="metric">
          <span class="value">{{ formatNumber(metrics.totalViews) }}</span>
          <span class="change" :class="{ 'positive': metrics.viewsGrowth > 0 }">
            {{ formatPercent(metrics.viewsGrowth) }}%
          </span>
        </div>
      </div>

      <div class="analytics-card">
        <h3>Average Engagement</h3>
        <div class="metric">
          <span class="value">{{ formatPercent(metrics.avgEngagement) }}%</span>
          <span class="change" :class="{ 'positive': metrics.engagementGrowth > 0 }">
            {{ formatPercent(metrics.engagementGrowth) }}%
          </span>
        </div>
      </div>

      <div class="analytics-card">
        <h3>Revenue</h3>
        <div class="metric">
          <span class="value">${{ formatNumber(metrics.revenue) }}</span>
          <span class="change" :class="{ 'positive': metrics.revenueGrowth > 0 }">
            {{ formatPercent(metrics.revenueGrowth) }}%
          </span>
        </div>
      </div>

      <!-- Charts -->
      <div class="chart-card wide">
        <h3>Growth Trends</h3>
        <div class="chart">
          <!-- Line chart component will go here -->
        </div>
      </div>

      <div class="chart-card">
        <h3>Engagement by Time</h3>
        <div class="chart">
          <!-- Bar chart component will go here -->
        </div>
      </div>

      <div class="chart-card">
        <h3>Content Performance</h3>
        <div class="chart">
          <!-- Pie chart component will go here -->
        </div>
      </div>

      <!-- Top Posts Table -->
      <div class="table-card wide">
        <h3>Top Performing Posts</h3>
        <table class="data-table">
          <thead>
            <tr>
              <th>Post</th>
              <th>Views</th>
              <th>Engagement</th>
              <th>CTR</th>
              <th>Revenue</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="post in topPosts" :key="post.id">
              <td>
                <div class="post-cell">
                  <img :src="post.image" :alt="post.title" class="post-thumbnail">
                  <div class="post-info">
                    <span class="post-title">{{ post.title }}</span>
                    <span class="post-date">{{ formatDate(post.date) }}</span>
                  </div>
                </div>
              </td>
              <td>{{ formatNumber(post.views) }}</td>
              <td>{{ formatPercent(post.engagement) }}%</td>
              <td>{{ formatPercent(post.ctr) }}%</td>
              <td>${{ formatNumber(post.revenue) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Data
const selectedChannel = ref('')
const selectedRange = ref('7d')
const channels = ref([])
const metrics = ref({
  totalSubscribers: 0,
  subscriberGrowth: 0,
  totalViews: 0,
  viewsGrowth: 0,
  avgEngagement: 0,
  engagementGrowth: 0,
  revenue: 0,
  revenueGrowth: 0
})
const topPosts = ref([])

// Constants
const dateRanges = [
  { label: '7 Days', value: '7d' },
  { label: '30 Days', value: '30d' },
  { label: '3 Months', value: '90d' },
  { label: '1 Year', value: '365d' }
]

// Methods
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
  return num.toFixed(1)
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
}

// Data fetching
const fetchAnalytics = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/analytics`, {
      params: {
        channelId: selectedChannel.value,
        range: selectedRange.value
      }
    })
    metrics.value = response.data.metrics
    topPosts.value = response.data.topPosts
  } catch (error) {
    console.error('Failed to fetch analytics:', error)
  }
}

const fetchChannels = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/channels`)
    channels.value = response.data
  } catch (error) {
    console.error('Failed to fetch channels:', error)
  }
}

// Watchers
watch([selectedChannel, selectedRange], () => {
  fetchAnalytics()
})

// Lifecycle
onMounted(() => {
  fetchChannels()
  fetchAnalytics()
})
</script>

<style scoped>
.analytics-view {
  padding: 2rem;
}

.analytics-header {
  margin-bottom: 2rem;
}

h1 {
  margin-bottom: 1rem;
}

.filters {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.channel-select {
  width: 200px;
}

.date-range {
  display: flex;
  gap: 0.5rem;
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.analytics-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart-card, .table-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.wide {
  grid-column: span 2;
}

.metric {
  display: flex;
  align-items: baseline;
  gap: 1rem;
}

.value {
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--text-color);
}

.change {
  font-size: 0.9rem;
  color: #dc3545;
}

.change.positive {
  color: #28a745;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.post-cell {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.post-thumbnail {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  object-fit: cover;
}

.post-info {
  display: flex;
  flex-direction: column;
}

.post-title {
  font-weight: 500;
}

.post-date {
  font-size: 0.8rem;
  color: var(--text-color);
  opacity: 0.8;
}

.chart {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--background-color);
  border-radius: 4px;
  margin-top: 1rem;
}
</style> 