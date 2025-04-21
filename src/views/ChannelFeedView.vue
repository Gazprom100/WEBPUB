<template>
  <div class="channel-feed-view">
    <div class="feed-header">
      <div class="feed-title">
        <h1>Лента новостей канала "{{ channelName }}"</h1>
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
      
      <div class="feed-actions">
        <button class="btn-add-post" @click="navigateToAddPost">
          <i class="fas fa-plus"></i> Создать публикацию
        </button>
        <button class="btn-export" @click="exportToExcel">
          <i class="fas fa-file-export"></i> Экспорт
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Загрузка ленты новостей...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchChannelFeed" class="btn-retry">Попробовать снова</button>
    </div>

    <div v-else class="feed-table-container">
      <div class="feed-table" ref="feedTableRef">
        <div class="feed-table-fixed-columns">
          <div class="fixed-column-header">
            <div class="fixed-column-cell header-cell">Канал "{{ channelName }}"</div>
            <div class="fixed-column-cell">Тема поста</div>
            <div class="fixed-column-cell">Акция</div>
            <div class="fixed-column-cell">Заголовок</div>
            <div class="fixed-column-cell row-text">Текст</div>
          </div>
          
          <div v-for="(row, rowIndex) in feedData" :key="rowIndex" class="fixed-column-row">
            <div class="fixed-column-cell">{{ row.section || '' }}</div>
          </div>
        </div>
        
        <div class="feed-table-content">
          <div class="feed-table-header">
            <div class="fixed-row-header">
              <div v-for="(day, dayIndex) in days" :key="dayIndex" class="day-column">
                <div class="day-cell">{{ day.date }}</div>
                <div class="day-icon">{{ day.icon }}</div>
              </div>
            </div>
          </div>
          
          <div class="feed-table-body">
            <div v-for="(row, rowIndex) in feedData" :key="rowIndex" class="feed-row">
              <div 
                v-for="(day, dayIndex) in days" 
                :key="dayIndex" 
                class="feed-cell"
                :class="{ 'has-post': getCellContent(rowIndex, dayIndex) }"
                @click="openPostEditor(rowIndex, dayIndex)"
              >
                <div v-if="getCellContent(rowIndex, dayIndex)" class="cell-content">
                  <div class="cell-title">{{ getCellContent(rowIndex, dayIndex).title }}</div>
                  <div v-if="getCellContent(rowIndex, dayIndex).description" class="cell-description">
                    {{ getCellContent(rowIndex, dayIndex).description }}
                  </div>
                  <div v-if="getCellContent(rowIndex, dayIndex).metrics" class="cell-metrics">
                    <div class="metric">
                      <i class="fas fa-eye"></i>
                      <span>{{ formatNumber(getCellContent(rowIndex, dayIndex).metrics.views) }}</span>
                    </div>
                    <div class="metric">
                      <i class="fas fa-thumbs-up"></i>
                      <span>{{ formatNumber(getCellContent(rowIndex, dayIndex).metrics.likes) }}</span>
                    </div>
                  </div>
                  <div v-if="getCellContent(rowIndex, dayIndex).time" class="cell-time">
                    {{ getCellContent(rowIndex, dayIndex).time }}
                  </div>
                </div>
                <div v-else class="cell-empty" @click.stop="createPost(rowIndex, dayIndex)">
                  <i class="fas fa-plus-circle"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const channelId = computed(() => route.params.id)
const feedTableRef = ref(null)

const channel = ref(null)
const channelName = ref('...')
const feedData = ref([])
const isLoading = ref(true)
const error = ref(null)

// Это должно быть динамически получено с сервера
// В демонстрационных целях создаем статические данные
const days = ref([
  { date: '01.02.22', icon: '♂️' },
  { date: '02.02.22', icon: '♀️' },
  { date: '03.02.22', icon: '♂️' },
  { date: '04.02.22', icon: '♀️' },
  { date: '05.02.22', icon: '♂️' },
  { date: '06.02.22', icon: '♀️' },
  { date: '07.02.22', icon: '♂️' },
  { date: '08.02.22', icon: '♀️' },
  { date: '09.02.22', icon: '♂️' },
  { date: '10.02.22', icon: '♀️' },
  { date: '11.02.22', icon: '♂️' },
  { date: '12.02.22', icon: '♀️' }
])

// Симуляция данных ленты новостей
// В реальном приложении эти данные должны приходить с сервера
const mockFeedData = [
  { 
    section: 'Описание',
    posts: [
      { day: 0, title: 'Школа KX', description: 'Описание курса школы KX' },
      { day: 3, title: 'Релокация', description: 'Подробная информация о релокации' },
      { day: 4, title: 'Тренировка', description: 'План тренировки на месяц' },
      { day: 5, title: 'Презентация', description: 'Презентация новых возможностей' },
      { day: 6, title: 'Международный женский день', description: 'Поздравления с 8 марта' },
      { day: 7, title: 'Спортивная школа', description: 'Открытие спортивной школы' }
    ] 
  },
  { 
    section: 'Акция',
    posts: [
      { day: 1, title: 'Обучение', description: 'Курсы повышения квалификации' },
      { day: 6, title: 'Поздравляем с 8 Марта!', description: 'С Праздником Вас, дорогие женщины!' },
    ] 
  },
  { 
    section: 'Заголовок',
    posts: [
      { day: 0, title: 'Вы уже достигли квалификации «Консультант»?', metrics: { views: 120, likes: 45 } },
      { day: 3, title: 'Такая еженедельная процедура поможет избежать конфликта планетных сил и неприятной энергетизации...', metrics: { views: 220, likes: 65 } },
      { day: 4, title: 'Такая еженедельная процедура поможет избежать конфликта планетных сил и неприятной энергетизации...', metrics: { views: 180, likes: 32 } },
      { day: 6, title: 'Вы осознанно решили строить карьеру и бизнес в Эйвон?', metrics: { views: 310, likes: 77 } },
    ] 
  },
  { 
    section: 'Текст',
    posts: [
      { day: 0, title: 'Поздравляем! 👏 Знаете у вас есть возможность достичь званием Консультант и узнать что именно...', time: '8:00' },
      { day: 3, title: 'Таро открывает нам, что в период растущей луны проблема конфликта...', time: '11:00' },
      { day: 4, title: 'Таро открывает нам, что в период растущей луны проблема конфликта...', time: '8:00' },
      { day: 6, title: 'Дорогие наши девушки! Компания Эйвон спешит поздравить вас с праздником!', time: '10:00' },
      { day: 8, title: 'Компания Эйвон спешит поздравить вас с Международным Женским днем ❤️', time: '10:00' },
    ] 
  }
]

onMounted(() => {
  fetchChannelInfo()
  fetchChannelFeed()
  
  // Обработчик горизонтального скролла для синхронизации заголовка
  if (feedTableRef.value) {
    const tableContent = feedTableRef.value.querySelector('.feed-table-content')
    if (tableContent) {
      tableContent.addEventListener('scroll', handleTableScroll)
    }
  }
})

const handleTableScroll = (event) => {
  const header = feedTableRef.value.querySelector('.feed-table-header')
  if (header) {
    header.scrollLeft = event.target.scrollLeft
  }
}

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

const fetchChannelFeed = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    // В реальном приложении заменить на фактический API endpoint
    // const response = await axios.get(`/api/channels/${channelId.value}/feed`)
    // feedData.value = response.data
    
    // Временная заглушка с демонстрационными данными
    setTimeout(() => {
      feedData.value = mockFeedData
      isLoading.value = false
    }, 800)
  } catch (err) {
    console.error('Ошибка при загрузке ленты новостей:', err)
    error.value = 'Не удалось загрузить ленту новостей канала.'
    isLoading.value = false
  }
}

const getCellContent = (rowIndex, dayIndex) => {
  const row = feedData.value[rowIndex]
  if (!row || !row.posts) return null
  
  const post = row.posts.find(post => post.day === dayIndex)
  return post || null
}

const navigateToAddPost = () => {
  router.push(`/channels/${channelId.value}/posts/new`)
}

const openPostEditor = (rowIndex, dayIndex) => {
  const post = getCellContent(rowIndex, dayIndex)
  if (post) {
    // В реальном приложении нужен ID поста
    const postId = `${rowIndex}-${dayIndex}`
    router.push(`/channels/${channelId.value}/posts/edit/${postId}`)
  }
}

const createPost = (rowIndex, dayIndex) => {
  const date = days.value[dayIndex].date
  const section = feedData.value[rowIndex].section
  router.push({
    path: `/channels/${channelId.value}/posts/new`,
    query: { date, section }
  })
}

const exportToExcel = () => {
  // Здесь должен быть код для экспорта ленты в Excel
  alert('Экспорт ленты новостей в Excel')
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
.channel-feed-view {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

.feed-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.feed-title h1 {
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

.feed-actions {
  display: flex;
  gap: 0.75rem;
}

.btn-add-post, .btn-export {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add-post {
  background-color: #4299E1;
  color: white;
  border: none;
}

.btn-add-post:hover {
  background-color: #3182CE;
}

.btn-export {
  background-color: transparent;
  border: 1px solid #CBD5E0;
  color: #4A5568;
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

.feed-table-container {
  overflow: hidden;
  border-radius: 10px;
  border: 1px solid #eaeaea;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.feed-table {
  display: flex;
  width: 100%;
  height: 100%;
  background-color: white;
}

.feed-table-fixed-columns {
  min-width: 200px;
  width: 200px;
  flex-shrink: 0;
  border-right: 1px solid #eaeaea;
  background-color: #f8f9fa;
  position: relative;
  z-index: 10;
}

.fixed-column-header {
  position: sticky;
  top: 0;
  background-color: #f1f5f9;
  z-index: 20;
}

.fixed-column-cell {
  height: 60px;
  padding: 0.75rem;
  border-bottom: 1px solid #eaeaea;
  display: flex;
  align-items: center;
  font-weight: 500;
}

.header-cell {
  background-color: #f1f5f9;
  font-weight: 600;
  color: #334155;
}

.row-text {
  height: 80px;
  align-items: flex-start;
}

.feed-table-content {
  flex-grow: 1;
  overflow-x: auto;
  position: relative;
}

.feed-table-header {
  overflow: hidden;
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: white;
}

.fixed-row-header {
  display: flex;
  border-bottom: 1px solid #eaeaea;
  background-color: #f1f5f9;
}

.day-column {
  min-width: 100px;
  flex-shrink: 0;
  height: 60px;
  padding: 0.6rem 0.5rem;
  border-right: 1px solid #eaeaea;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.day-cell {
  font-weight: 600;
  font-size: 0.85rem;
  color: #334155;
}

.day-icon {
  font-size: 1.2rem;
  margin-top: 0.2rem;
}

.feed-table-body {
  display: flex;
  flex-direction: column;
}

.feed-row {
  display: flex;
  border-bottom: 1px solid #eaeaea;
}

.feed-cell {
  min-width: 100px;
  flex-shrink: 0;
  height: 60px;
  padding: 0.5rem;
  border-right: 1px solid #eaeaea;
  background-color: white;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: background-color 0.15s;
}

.feed-row:last-child .feed-cell {
  height: 80px;
}

.feed-cell:hover {
  background-color: #f8fafc;
}

.has-post {
  background-color: #edf2f7;
}

.has-post:hover {
  background-color: #e2e8f0;
}

.cell-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-size: 0.8rem;
}

.cell-title {
  font-weight: 500;
  margin-bottom: 0.2rem;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.cell-description {
  font-size: 0.75rem;
  color: #4a5568;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
}

.cell-metrics {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.3rem;
  font-size: 0.75rem;
  color: #718096;
}

.metric {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.cell-time {
  font-size: 0.75rem;
  color: #718096;
  text-align: right;
  margin-top: 0.2rem;
}

.cell-empty {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a0aec0;
  transition: color 0.2s;
}

.cell-empty:hover {
  color: #4299E1;
}

.cell-empty i {
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .feed-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .feed-actions {
    width: 100%;
  }
  
  .btn-add-post, .btn-export {
    flex: 1;
  }
}
</style> 