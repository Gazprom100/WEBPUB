<template>
  <div class="notifications-panel" v-if="isOpen">
    <div class="notifications-header">
      <h3>Уведомления</h3>
      <div class="header-actions">
        <button class="btn-text" @click="markAllAsRead" v-if="hasUnread">
          Отметить все как прочитанные
        </button>
        <button class="btn-close" @click="close">×</button>
      </div>
    </div>

    <div class="notifications-content" v-if="notifications.length">
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        class="notification-item"
        :class="{ 'unread': !notification.read }"
        @click="handleNotificationClick(notification)"
      >
        <div class="notification-icon" :class="notification.type">
          <span v-if="notification.type === 'success'">✓</span>
          <span v-else-if="notification.type === 'warning'">!</span>
          <span v-else-if="notification.type === 'info'">i</span>
          <span v-else>🔔</span>
        </div>
        <div class="notification-content">
          <div class="notification-title">{{ notification.title }}</div>
          <div class="notification-message">{{ notification.message }}</div>
          <div class="notification-time">{{ formatTime(notification.createdAt) }}</div>
        </div>
      </div>
    </div>

    <div class="notifications-empty" v-else>
      <div class="empty-icon">🔔</div>
      <p>У вас нет новых уведомлений</p>
    </div>

    <div class="notifications-footer">
      <button class="btn-text" @click="loadMore" v-if="hasMore">
        Загрузить еще
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useNotificationsStore } from '@/stores/notifications'
import { formatDistanceToNow } from 'date-fns'
import { ru } from 'date-fns/locale'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close'])

const notificationsStore = useNotificationsStore()
const notifications = computed(() => notificationsStore.notifications)
const hasUnread = computed(() => notifications.value.some(n => !n.read))
const hasMore = computed(() => notificationsStore.hasMore)

const close = () => {
  emit('close')
}

const handleNotificationClick = async (notification) => {
  if (!notification.read) {
    await notificationsStore.markAsRead(notification.id)
  }
  
  // Обработка действия уведомления
  if (notification.action) {
    if (notification.action.type === 'link') {
      window.location.href = notification.action.url
    } else if (notification.action.type === 'function') {
      notification.action.handler()
    }
  }
}

const markAllAsRead = async () => {
  await notificationsStore.markAllAsRead()
}

const loadMore = async () => {
  await notificationsStore.loadMore()
}

const formatTime = (date) => {
  return formatDistanceToNow(new Date(date), { addSuffix: true, locale: ru })
}
</script>

<style scoped>
.notifications-panel {
  position: absolute;
  top: 60px;
  right: 20px;
  width: 380px;
  max-height: 600px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  z-index: 1000;
}

.notifications-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notifications-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn-text {
  background: none;
  border: none;
  color: var(--primary-color);
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  padding: 0;
  cursor: pointer;
  opacity: 0.6;
}

.btn-close:hover {
  opacity: 1;
}

.notifications-content {
  overflow-y: auto;
  flex-grow: 1;
}

.notification-item {
  padding: 1rem;
  display: flex;
  gap: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
  border-bottom: 1px solid var(--border-color);
}

.notification-item:hover {
  background-color: var(--hover-color);
}

.notification-item.unread {
  background-color: var(--unread-color);
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 1rem;
}

.notification-icon.success {
  background-color: var(--success-color);
  color: white;
}

.notification-icon.warning {
  background-color: var(--warning-color);
  color: white;
}

.notification-icon.info {
  background-color: var(--info-color);
  color: white;
}

.notification-content {
  flex-grow: 1;
}

.notification-title {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.notification-message {
  font-size: 0.9rem;
  color: var(--text-color);
  opacity: 0.8;
  margin-bottom: 0.5rem;
}

.notification-time {
  font-size: 0.8rem;
  color: var(--text-color);
  opacity: 0.6;
}

.notifications-empty {
  padding: 3rem 1rem;
  text-align: center;
  color: var(--text-color);
  opacity: 0.6;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.notifications-footer {
  padding: 1rem;
  border-top: 1px solid var(--border-color);
  text-align: center;
}
</style> 