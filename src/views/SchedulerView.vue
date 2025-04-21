<template>
  <div class="scheduler-view">
    <div class="scheduler-header">
      <h1>Планировщик публикаций</h1>
      <div class="header-actions">
        <div class="channel-selector">
          <label for="channelSelect">Канал:</label>
          <select id="channelSelect" v-model="selectedChannel" class="select-control">
            <option v-for="channel in channels" :key="channel.id" :value="channel.id">
              {{ channel.name }}
            </option>
          </select>
        </div>
        <button class="btn-primary" @click="createPost">
          <i class="fas fa-plus"></i> Создать публикацию
        </button>
      </div>
    </div>

    <div class="calendar-controls">
      <div class="calendar-nav">
        <button class="btn-icon" @click="prevMonth">
          <i class="fas fa-chevron-left"></i>
        </button>
        <h2 class="current-month">{{ currentMonthName }} {{ currentYear }}</h2>
        <button class="btn-icon" @click="nextMonth">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
      <div class="view-controls">
        <button 
          class="view-btn" 
          :class="{ 'active': currentView === 'month' }" 
          @click="currentView = 'month'"
        >
          Месяц
        </button>
        <button 
          class="view-btn" 
          :class="{ 'active': currentView === 'week' }" 
          @click="currentView = 'week'"
        >
          Неделя
        </button>
        <button 
          class="view-btn" 
          :class="{ 'active': currentView === 'day' }" 
          @click="currentView = 'day'"
        >
          День
        </button>
      </div>
    </div>

    <!-- Месячный вид календаря -->
    <div v-if="currentView === 'month'" class="calendar-month">
      <div class="weekdays">
        <div class="weekday" v-for="day in weekdays" :key="day">{{ day }}</div>
      </div>
      <div class="days">
        <div 
          v-for="(day, index) in calendarDays" 
          :key="index"
          class="day"
          :class="{ 
            'other-month': !day.isCurrentMonth, 
            'today': day.isToday,
            'has-posts': day.posts.length > 0
          }"
          @click="selectDay(day)"
        >
          <div class="day-header">
            <span class="day-number">{{ day.day }}</span>
            <span v-if="day.isToday" class="day-indicator">Сегодня</span>
          </div>
          <div class="day-posts">
            <div 
              v-for="(post, postIndex) in day.posts.slice(0, 3)" 
              :key="postIndex"
              class="day-post"
              :class="post.status"
              @click.stop="openPost(post)"
            >
              <span class="post-time">{{ formatTime(post.publishTime) }}</span>
              <span class="post-title">{{ post.title }}</span>
            </div>
            <div v-if="day.posts.length > 3" class="more-posts">
              +{{ day.posts.length - 3 }} еще
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Недельный вид календаря -->
    <div v-else-if="currentView === 'week'" class="calendar-week">
      <div class="week-header">
        <div class="time-column"></div>
        <div 
          v-for="(day, index) in weekDays" 
          :key="index" 
          class="day-column"
          :class="{ 'today': day.isToday }"
        >
          <div class="day-name">{{ weekdays[day.dayOfWeek] }}</div>
          <div class="day-number">{{ day.day }}</div>
        </div>
      </div>
      <div class="week-grid">
        <div class="time-slots">
          <div v-for="hour in 24" :key="hour" class="time-slot">
            <div class="time-label">{{ formatHour(hour - 1) }}</div>
          </div>
        </div>
        <div class="week-content">
          <div 
            v-for="(day, dayIndex) in weekDays" 
            :key="dayIndex" 
            class="day-slots"
            :class="{ 'today': day.isToday }"
          >
            <div 
              v-for="hour in 24" 
              :key="`${dayIndex}-${hour}`" 
              class="hour-slot"
              @click="createPostAt(day.date, hour - 1)"
            >
              <div 
                v-for="(post, postIndex) in getPostsForHour(day, hour - 1)" 
                :key="postIndex"
                class="week-post"
                :class="post.status"
                :style="{
                  top: `${(post.publishTime.getMinutes() / 60) * 100}%`,
                  height: `${post.durationMinutes / 60 * 100}%`
                }"
                @click.stop="openPost(post)"
              >
                <div class="post-time">{{ formatTime(post.publishTime) }}</div>
                <div class="post-title">{{ post.title }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Дневной вид календаря -->
    <div v-else class="calendar-day">
      <div class="day-header">
        <div class="selected-day">
          {{ formatFullDate(selectedDate) }}
          <span v-if="isToday(selectedDate)" class="today-marker">Сегодня</span>
        </div>
      </div>
      <div class="day-grid">
        <div class="time-slots">
          <div v-for="hour in 24" :key="hour" class="time-slot">
            <div class="time-label">{{ formatHour(hour - 1) }}</div>
          </div>
        </div>
        <div class="day-content">
          <div 
            v-for="hour in 24" 
            :key="hour" 
            class="hour-slot"
            @click="createPostAt(selectedDate, hour - 1)"
          >
            <div 
              v-for="(post, index) in getPostsForHour({ date: selectedDate }, hour - 1)" 
              :key="index"
              class="day-post"
              :class="post.status"
              :style="{
                top: `${(post.publishTime.getMinutes() / 60) * 100}%`,
                height: `${post.durationMinutes / 60 * 100}%`
              }"
              @click.stop="openPost(post)"
            >
              <div class="post-time">{{ formatTime(post.publishTime) }}</div>
              <div class="post-title">{{ post.title }}</div>
              <div class="post-channel">{{ getChannelName(post.channelId) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Панель выбранного дня -->
    <div v-if="selectedDay && currentView === 'month'" class="day-panel">
      <div class="panel-header">
        <h3>{{ formatFullDate(selectedDay.date) }}</h3>
        <button class="btn-close" @click="selectedDay = null">×</button>
      </div>
      <div class="day-posts-list">
        <div v-if="selectedDay.posts.length === 0" class="no-posts">
          <p>Нет запланированных публикаций</p>
          <button class="btn-primary" @click="createPostAt(selectedDay.date)">
            Создать публикацию
          </button>
        </div>
        <div v-else>
          <div 
            v-for="(post, index) in selectedDay.posts" 
            :key="index"
            class="day-post-item"
            :class="post.status"
          >
            <div class="post-time">{{ formatTime(post.publishTime) }}</div>
            <div class="post-info">
              <div class="post-title">{{ post.title }}</div>
              <div class="post-meta">
                <span class="post-channel">{{ getChannelName(post.channelId) }}</span>
                <span class="post-status">{{ getStatusText(post.status) }}</span>
              </div>
            </div>
            <div class="post-actions">
              <button class="btn-action" @click="openPost(post)">
                <i class="fas fa-edit"></i>
              </button>
              <button class="btn-action" @click="deletePost(post)">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
          <div class="add-post-btn">
            <button class="btn-outline" @click="createPostAt(selectedDay.date)">
              <i class="fas fa-plus"></i> Добавить публикацию
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Данные каналов (в реальном приложении должны загружаться из API)
const channels = ref([
  { id: '1', name: 'Spacebot' },
  { id: '2', name: 'Marketing Channel' },
  { id: '3', name: 'Tech News' }
])
const selectedChannel = ref('1')

// Управление видом календаря
const currentView = ref('month')
const currentMonth = ref(new Date().getMonth())
const currentYear = ref(new Date().getFullYear())
const selectedDate = ref(new Date())
const selectedDay = ref(null)

// Вспомогательные данные
const weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
const monthNames = [
  'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
  'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
]

// Тестовые данные публикаций
const posts = ref([
  {
    id: '1',
    title: 'Как достичь звания Консультант за 30 дней',
    channelId: '1',
    publishTime: new Date(new Date().setHours(10, 0, 0, 0)),
    status: 'scheduled',
    durationMinutes: 30
  },
  {
    id: '2',
    title: 'Международный женский день',
    channelId: '1',
    publishTime: new Date(new Date().setHours(14, 30, 0, 0)),
    status: 'published',
    durationMinutes: 30
  },
  {
    id: '3',
    title: 'Новая коллекция продуктов',
    channelId: '1',
    publishTime: new Date(new Date().setDate(new Date().getDate() + 1)),
    status: 'draft',
    durationMinutes: 45
  },
  {
    id: '4',
    title: 'Обучение: новые техники продаж',
    channelId: '1',
    publishTime: new Date(new Date().setDate(new Date().getDate() + 3)),
    status: 'scheduled',
    durationMinutes: 30
  }
])

// Вычисляемые свойства
const currentMonthName = computed(() => monthNames[currentMonth.value])

const calendarDays = computed(() => {
  const days = []
  const firstDay = new Date(currentYear.value, currentMonth.value, 1)
  
  // Определяем день недели первого дня месяца (0 - воскресенье, 6 - суббота)
  let firstDayOfWeek = firstDay.getDay()
  // Преобразуем в формат 0 - понедельник, 6 - воскресенье
  firstDayOfWeek = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1
  
  // Добавляем дни предыдущего месяца
  const prevMonthDays = firstDayOfWeek
  const prevMonth = new Date(currentYear.value, currentMonth.value, 0)
  const prevMonthLastDay = prevMonth.getDate()
  
  for (let i = prevMonthDays - 1; i >= 0; i--) {
    const day = prevMonthLastDay - i
    const date = new Date(currentYear.value, currentMonth.value - 1, day)
    days.push({
      day,
      date,
      isCurrentMonth: false,
      isToday: isSameDay(date, new Date()),
      posts: getPostsForDay(date)
    })
  }
  
  // Добавляем дни текущего месяца
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0)
  const daysInMonth = lastDay.getDate()
  
  for (let i = 1; i <= daysInMonth; i++) {
    const date = new Date(currentYear.value, currentMonth.value, i)
    days.push({
      day: i,
      date,
      isCurrentMonth: true,
      isToday: isSameDay(date, new Date()),
      posts: getPostsForDay(date)
    })
  }
  
  // Добавляем дни следующего месяца для заполнения сетки (всего 42 ячейки)
  const remainingDays = 42 - days.length
  for (let i = 1; i <= remainingDays; i++) {
    const date = new Date(currentYear.value, currentMonth.value + 1, i)
    days.push({
      day: i,
      date,
      isCurrentMonth: false,
      isToday: isSameDay(date, new Date()),
      posts: getPostsForDay(date)
    })
  }
  
  return days
})

const weekDays = computed(() => {
  const days = []
  const startOfWeek = new Date(selectedDate.value)
  const dayOfWeek = startOfWeek.getDay()
  
  // Корректируем на понедельник как первый день недели
  const diff = dayOfWeek === 0 ? -6 : 1 - dayOfWeek
  startOfWeek.setDate(startOfWeek.getDate() + diff)
  
  for (let i = 0; i < 7; i++) {
    const date = new Date(startOfWeek)
    date.setDate(startOfWeek.getDate() + i)
    days.push({
      day: date.getDate(),
      date,
      isToday: isSameDay(date, new Date()),
      dayOfWeek: i
    })
  }
  
  return days
})

// Методы
const prevMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

const selectDay = (day) => {
  selectedDay.value = day
}

const isSameDay = (date1, date2) => {
  return date1.getDate() === date2.getDate() &&
         date1.getMonth() === date2.getMonth() &&
         date1.getFullYear() === date2.getFullYear()
}

const isToday = (date) => {
  return isSameDay(date, new Date())
}

const getPostsForDay = (date) => {
  return posts.value.filter(post => isSameDay(post.publishTime, date))
}

const getPostsForHour = (day, hour) => {
  return posts.value.filter(post => 
    isSameDay(post.publishTime, day.date) && 
    post.publishTime.getHours() === hour
  )
}

const formatTime = (date) => {
  return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

const formatHour = (hour) => {
  return `${hour}:00`
}

const formatFullDate = (date) => {
  return date.toLocaleDateString('ru-RU', { 
    weekday: 'long', 
    day: 'numeric', 
    month: 'long', 
    year: 'numeric' 
  })
}

const getChannelName = (channelId) => {
  const channel = channels.value.find(c => c.id === channelId)
  return channel ? channel.name : ''
}

const getStatusText = (status) => {
  switch (status) {
    case 'published': return 'Опубликовано'
    case 'scheduled': return 'Запланировано'
    case 'draft': return 'Черновик'
    default: return status
  }
}

const createPost = () => {
  router.push(`/channels/${selectedChannel.value}/posts/new`)
}

const createPostAt = (date, hour = 12) => {
  const scheduledTime = new Date(date)
  scheduledTime.setHours(hour, 0, 0, 0)
  
  router.push({
    path: `/channels/${selectedChannel.value}/posts/new`,
    query: { 
      scheduledTime: scheduledTime.toISOString(),
    }
  })
}

const openPost = (post) => {
  router.push(`/channels/${post.channelId}/posts/edit/${post.id}`)
}

const deletePost = (post) => {
  if (confirm('Вы уверены, что хотите удалить эту публикацию?')) {
    posts.value = posts.value.filter(p => p.id !== post.id)
  }
}

onMounted(() => {
  // Инициализация
})
</script>

<style scoped>
.scheduler-view {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

.scheduler-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.scheduler-header h1 {
  font-size: 1.8rem;
  margin: 0;
  color: #1a202c;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.channel-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.select-control {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  min-width: 200px;
}

.btn-primary {
  background-color: #4299e1;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.6rem 1rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #3182ce;
}

.calendar-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.calendar-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.current-month {
  font-size: 1.25rem;
  margin: 0;
  font-weight: 600;
}

.btn-icon {
  background: none;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-icon:hover {
  background-color: #edf2f7;
}

.view-controls {
  display: flex;
  background-color: #edf2f7;
  border-radius: 6px;
  overflow: hidden;
}

.view-btn {
  background: none;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.view-btn.active {
  background-color: #4299e1;
  color: white;
}

/* Месячный вид */
.calendar-month {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background-color: #f7fafc;
  border-bottom: 1px solid #e2e8f0;
}

.weekday {
  padding: 0.75rem;
  text-align: center;
  font-weight: 500;
  color: #4a5568;
}

.days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-template-rows: repeat(6, 1fr);
  min-height: 600px;
}

.day {
  border-right: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
  padding: 0.5rem;
  cursor: pointer;
  position: relative;
  transition: background-color 0.15s;
}

.day:nth-child(7n) {
  border-right: none;
}

.day:nth-last-child(-n+7) {
  border-bottom: none;
}

.day:hover {
  background-color: #f7fafc;
}

.other-month {
  color: #a0aec0;
  background-color: #f8f9fa;
}

.today {
  background-color: #ebf8ff;
}

.has-posts::after {
  content: '';
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 8px;
  height: 8px;
  background-color: #4299e1;
  border-radius: 50%;
}

.day-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.day-number {
  font-weight: 500;
}

.day-indicator {
  font-size: 0.75rem;
  background-color: #4299e1;
  color: white;
  padding: 0.1rem 0.35rem;
  border-radius: 10px;
}

.day-posts {
  font-size: 0.85rem;
}

.day-post {
  margin-bottom: 0.35rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  background-color: #e6f6ff;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.day-post:hover {
  opacity: 0.9;
}

.day-post.published {
  background-color: #c6f6d5;
}

.day-post.draft {
  background-color: #e9ecef;
}

.day-post.scheduled {
  background-color: #bee3f8;
}

.post-time {
  font-weight: 500;
  margin-right: 0.5rem;
}

.post-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.more-posts {
  font-size: 0.75rem;
  color: #718096;
  text-align: center;
  padding: 0.25rem;
}

/* Недельный вид */
.calendar-week {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.week-header {
  display: flex;
  border-bottom: 1px solid #e2e8f0;
}

.time-column {
  width: 60px;
  flex-shrink: 0;
  border-right: 1px solid #e2e8f0;
}

.day-column {
  flex: 1;
  padding: 0.75rem;
  text-align: center;
  background-color: #f7fafc;
}

.day-column.today {
  background-color: #ebf8ff;
}

.day-name {
  font-weight: 500;
  color: #4a5568;
}

.day-number {
  font-size: 1.25rem;
  font-weight: 600;
}

.week-grid {
  display: flex;
  height: 600px;
  overflow-y: auto;
}

.time-slots {
  width: 60px;
  flex-shrink: 0;
  border-right: 1px solid #e2e8f0;
}

.time-slot {
  height: 60px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.time-label {
  font-size: 0.75rem;
  color: #718096;
}

.week-content {
  display: flex;
  flex: 1;
}

.day-slots {
  flex: 1;
  position: relative;
  border-right: 1px solid #e2e8f0;
}

.day-slots:last-child {
  border-right: none;
}

.day-slots.today {
  background-color: #ebf8ff;
}

.hour-slot {
  height: 60px;
  border-bottom: 1px solid #e2e8f0;
  position: relative;
}

.week-post {
  position: absolute;
  left: 2px;
  right: 2px;
  padding: 0.25rem;
  border-radius: 4px;
  font-size: 0.75rem;
  z-index: 1;
  overflow: hidden;
  cursor: pointer;
}

.week-post.published {
  background-color: #c6f6d5;
}

.week-post.draft {
  background-color: #e9ecef;
}

.week-post.scheduled {
  background-color: #bee3f8;
}

/* Дневной вид */
.calendar-day {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.day-header {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  background-color: #f7fafc;
}

.selected-day {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
}

.today-marker {
  font-size: 0.85rem;
  background-color: #4299e1;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  margin-left: 0.5rem;
  vertical-align: middle;
}

.day-grid {
  display: flex;
  height: 600px;
  overflow-y: auto;
}

.day-content {
  flex: 1;
}

.day-post {
  position: absolute;
  left: 4px;
  right: 4px;
  padding: 0.35rem;
  border-radius: 4px;
  z-index: 1;
  overflow: hidden;
  cursor: pointer;
}

.day-post.published {
  background-color: #c6f6d5;
}

.day-post.draft {
  background-color: #e9ecef;
}

.day-post.scheduled {
  background-color: #bee3f8;
}

.post-channel {
  font-size: 0.75rem;
  color: #718096;
}

/* Панель выбранного дня */
.day-panel {
  position: fixed;
  right: 1.5rem;
  top: 6rem;
  width: 350px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.panel-header {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  color: #718096;
}

.day-posts-list {
  padding: 1rem;
  max-height: 400px;
  overflow-y: auto;
}

.no-posts {
  text-align: center;
  padding: 2rem 0;
  color: #718096;
}

.day-post-item {
  display: flex;
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 0.75rem;
  background-color: #f7fafc;
}

.day-post-item.published {
  border-left: 3px solid #38a169;
}

.day-post-item.draft {
  border-left: 3px solid #718096;
}

.day-post-item.scheduled {
  border-left: 3px solid #3182ce;
}

.post-info {
  flex: 1;
  margin: 0 0.75rem;
}

.post-meta {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: #718096;
}

.post-status {
  padding: 0.15rem 0.35rem;
  border-radius: 4px;
  background-color: #edf2f7;
}

.post-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.btn-action {
  background: none;
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-action:hover {
  background-color: #edf2f7;
}

.add-post-btn {
  margin-top: 1rem;
  text-align: center;
}

.btn-outline {
  background: none;
  border: 1px solid #4299e1;
  color: #4299e1;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.btn-outline:hover {
  background-color: #ebf8ff;
}

/* Адаптивность */
@media (max-width: 768px) {
  .scheduler-header,
  .calendar-controls {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .header-actions {
    width: 100%;
    flex-direction: column;
  }
  
  .channel-selector {
    width: 100%;
  }
  
  .select-control {
    width: 100%;
  }
  
  .btn-primary {
    width: 100%;
    justify-content: center;
  }
  
  .day-panel {
    position: fixed;
    left: 1rem;
    right: 1rem;
    top: 6rem;
    width: auto;
  }
}
</style> 