<template>
  <div class="settings-view">
    <div class="settings-header">
      <h1>Настройки</h1>
    </div>

    <div class="settings-content">
      <!-- Профиль -->
      <div class="settings-section">
        <h2>Профиль</h2>
        <form @submit.prevent="updateProfile" class="settings-form">
          <div class="form-group">
            <label>Фото профиля</label>
            <div class="avatar-upload">
              <img :src="avatar || '/default-avatar.png'" alt="Avatar" class="avatar-preview">
              <input 
                type="file" 
                ref="avatarInput"
                accept="image/*"
                @change="handleAvatarChange"
                class="avatar-input"
              >
              <button type="button" class="btn btn-secondary" @click="triggerAvatarUpload">
                Изменить фото
              </button>
            </div>
          </div>

          <div class="form-group">
            <label>Имя</label>
            <input 
              type="text" 
              v-model="profile.name"
              class="form-input"
              placeholder="Ваше имя"
            >
          </div>

          <div class="form-group">
            <label>Email</label>
            <input 
              type="email" 
              v-model="profile.email"
              class="form-input"
              placeholder="your@email.com"
              disabled
            >
            <span class="input-hint">Email нельзя изменить</span>
          </div>

          <div class="form-group">
            <label>Описание</label>
            <textarea 
              v-model="profile.bio"
              class="form-input"
              rows="4"
              placeholder="Расскажите о себе"
            ></textarea>
          </div>

          <button type="submit" class="btn btn-primary" :disabled="isUpdating">
            {{ isUpdating ? 'Сохранение...' : 'Сохранить изменения' }}
          </button>
        </form>
      </div>

      <!-- Безопасность -->
      <div class="settings-section">
        <h2>Безопасность</h2>
        <form @submit.prevent="updatePassword" class="settings-form">
          <div class="form-group">
            <label>Текущий пароль</label>
            <input 
              type="password" 
              v-model="passwords.current"
              class="form-input"
              placeholder="••••••••"
            >
          </div>

          <div class="form-group">
            <label>Новый пароль</label>
            <input 
              type="password" 
              v-model="passwords.new"
              class="form-input"
              placeholder="••••••••"
            >
          </div>

          <div class="form-group">
            <label>Подтвердите новый пароль</label>
            <input 
              type="password" 
              v-model="passwords.confirm"
              class="form-input"
              placeholder="••••••••"
            >
          </div>

          <button type="submit" class="btn btn-primary" :disabled="isUpdatingPassword">
            {{ isUpdatingPassword ? 'Обновление...' : 'Обновить пароль' }}
          </button>
        </form>
      </div>

      <!-- Уведомления -->
      <div class="settings-section">
        <h2>Уведомления</h2>
        <div class="settings-form">
          <div class="notification-setting">
            <div class="setting-info">
              <h3>Email уведомления</h3>
              <p>Получать уведомления на email</p>
            </div>
            <label class="switch">
              <input 
                type="checkbox" 
                v-model="notifications.email"
                @change="updateNotificationSettings"
              >
              <span class="slider"></span>
            </label>
          </div>

          <div class="notification-setting">
            <div class="setting-info">
              <h3>Push уведомления</h3>
              <p>Получать push-уведомления в браузере</p>
            </div>
            <label class="switch">
              <input 
                type="checkbox" 
                v-model="notifications.push"
                @change="updateNotificationSettings"
              >
              <span class="slider"></span>
            </label>
          </div>

          <div class="notification-types">
            <h3>Типы уведомлений</h3>
            <div class="checkbox-group">
              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  v-model="notifications.types.posts"
                  @change="updateNotificationSettings"
                >
                Новые посты
              </label>

              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  v-model="notifications.types.comments"
                  @change="updateNotificationSettings"
                >
                Комментарии
              </label>

              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  v-model="notifications.types.analytics"
                  @change="updateNotificationSettings"
                >
                Аналитика
              </label>

              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  v-model="notifications.types.monetization"
                  @change="updateNotificationSettings"
                >
                Монетизация
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Интеграции -->
      <div class="settings-section">
        <h2>Интеграции</h2>
        <div class="integrations-list">
          <div class="integration-item" v-for="integration in integrations" :key="integration.id">
            <div class="integration-info">
              <img :src="integration.icon" :alt="integration.name" class="integration-icon">
              <div>
                <h3>{{ integration.name }}</h3>
                <p>{{ integration.description }}</p>
              </div>
            </div>
            <button 
              class="btn" 
              :class="integration.connected ? 'btn-danger' : 'btn-primary'"
              @click="toggleIntegration(integration)"
            >
              {{ integration.connected ? 'Отключить' : 'Подключить' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const authStore = useAuthStore()

// Состояния
const avatar = ref(null)
const isUpdating = ref(false)
const isUpdatingPassword = ref(false)

const profile = reactive({
  name: '',
  email: '',
  bio: ''
})

const passwords = reactive({
  current: '',
  new: '',
  confirm: ''
})

const notifications = reactive({
  email: true,
  push: false,
  types: {
    posts: true,
    comments: true,
    analytics: true,
    monetization: true
  }
})

const integrations = ref([
  {
    id: 'telegram',
    name: 'Telegram',
    description: 'Автоматическая публикация в Telegram-канал',
    icon: '/icons/telegram.svg',
    connected: false
  },
  {
    id: 'instagram',
    name: 'Instagram',
    description: 'Кросспостинг в Instagram',
    icon: '/icons/instagram.svg',
    connected: false
  },
  {
    id: 'facebook',
    name: 'Facebook',
    description: 'Публикация на Facebook странице',
    icon: '/icons/facebook.svg',
    connected: false
  }
])

// Методы
const triggerAvatarUpload = () => {
  document.querySelector('.avatar-input').click()
}

const handleAvatarChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('avatar', file)

  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/users/avatar`, formData)
    avatar.value = response.data.avatarUrl
  } catch (error) {
    console.error('Ошибка при загрузке аватара:', error)
  }
}

const updateProfile = async () => {
  isUpdating.value = true
  try {
    await authStore.updateProfile({
      name: profile.name,
      bio: profile.bio
    })
  } catch (error) {
    console.error('Ошибка при обновлении профиля:', error)
  } finally {
    isUpdating.value = false
  }
}

const updatePassword = async () => {
  if (passwords.new !== passwords.confirm) {
    alert('Пароли не совпадают')
    return
  }

  isUpdatingPassword.value = true
  try {
    await axios.put(`${import.meta.env.VITE_API_URL}/auth/password`, {
      currentPassword: passwords.current,
      newPassword: passwords.new
    })
    
    // Очистка полей
    passwords.current = ''
    passwords.new = ''
    passwords.confirm = ''
  } catch (error) {
    console.error('Ошибка при обновлении пароля:', error)
  } finally {
    isUpdatingPassword.value = false
  }
}

const updateNotificationSettings = async () => {
  try {
    await axios.put(`${import.meta.env.VITE_API_URL}/users/notifications`, notifications)
  } catch (error) {
    console.error('Ошибка при обновлении настроек уведомлений:', error)
  }
}

const toggleIntegration = async (integration) => {
  try {
    if (integration.connected) {
      await axios.delete(`${import.meta.env.VITE_API_URL}/integrations/${integration.id}`)
      integration.connected = false
    } else {
      await axios.post(`${import.meta.env.VITE_API_URL}/integrations/${integration.id}`)
      integration.connected = true
    }
  } catch (error) {
    console.error('Ошибка при управлении интеграцией:', error)
  }
}

// Загрузка данных
onMounted(async () => {
  try {
    // Загрузка профиля
    const profileResponse = await axios.get(`${import.meta.env.VITE_API_URL}/users/profile`)
    const userData = profileResponse.data
    
    profile.name = userData.name
    profile.email = userData.email
    profile.bio = userData.bio
    avatar.value = userData.avatar

    // Загрузка настроек уведомлений
    const notificationsResponse = await axios.get(`${import.meta.env.VITE_API_URL}/users/notifications`)
    Object.assign(notifications, notificationsResponse.data)

    // Загрузка статуса интеграций
    const integrationsResponse = await axios.get(`${import.meta.env.VITE_API_URL}/integrations`)
    const connectedIntegrations = integrationsResponse.data
    
    integrations.value = integrations.value.map(integration => ({
      ...integration,
      connected: connectedIntegrations.includes(integration.id)
    }))
  } catch (error) {
    console.error('Ошибка при загрузке настроек:', error)
  }
})
</script>

<style scoped>
.settings-view {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.settings-header {
  margin-bottom: 2rem;
}

.settings-section {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.settings-section h2 {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.settings-form {
  max-width: 600px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
}

.input-hint {
  display: block;
  font-size: 0.875rem;
  color: var(--text-color);
  opacity: 0.7;
  margin-top: 0.25rem;
}

.avatar-upload {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar-preview {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-input {
  display: none;
}

.notification-setting {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid var(--border-color);
}

.setting-info h3 {
  margin: 0;
  font-size: 1rem;
}

.setting-info p {
  margin: 0.25rem 0 0;
  font-size: 0.875rem;
  color: var(--text-color);
  opacity: 0.7;
}

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: var(--primary-color);
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.notification-types {
  margin-top: 2rem;
}

.checkbox-group {
  display: grid;
  gap: 1rem;
  margin-top: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.integrations-list {
  display: grid;
  gap: 1rem;
}

.integration-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
}

.integration-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.integration-icon {
  width: 32px;
  height: 32px;
}

.integration-info h3 {
  margin: 0;
  font-size: 1rem;
}

.integration-info p {
  margin: 0.25rem 0 0;
  font-size: 0.875rem;
  color: var(--text-color);
  opacity: 0.7;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-secondary {
  background: var(--background-color);
  color: var(--text-color);
}

.btn-danger {
  background: var(--error-color);
  color: white;
}

.btn:hover:not(:disabled) {
  opacity: 0.9;
}
</style> 