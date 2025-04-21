<template>
  <div class="bot-settings-view">
    <div class="settings-header">
      <h1>Настройки Telegram-бота</h1>
      <p class="subtitle">Настройте токен бота и управляйте автопубликацией</p>
    </div>

    <div class="settings-card">
      <div class="card-header">
        <h2>Подключение бота</h2>
        <div class="bot-status" :class="{ 'connected': botConnected }">
          <span class="status-dot"></span>
          <span>{{ botConnected ? 'Подключен' : 'Не подключен' }}</span>
        </div>
      </div>

      <div class="settings-form">
        <div class="form-section">
          <label class="form-label">Токен бота</label>
          <div class="token-input">
            <input 
              :type="showToken ? 'text' : 'password'" 
              v-model="botToken" 
              class="form-input" 
              placeholder="Введите токен бота от BotFather"
              :disabled="botConnected"
            >
            <button type="button" class="toggle-btn" @click="showToken = !showToken">
              <span class="icon">{{ showToken ? '👁️' : '🔒' }}</span>
            </button>
          </div>
          <p class="help-text">
            Получите токен бота у <a href="https://t.me/BotFather" target="_blank">@BotFather</a> в Telegram
          </p>
        </div>

        <div class="form-section">
          <label class="form-label">Username бота</label>
          <input 
            type="text" 
            v-model="botUsername" 
            class="form-input" 
            placeholder="например, @your_bot"
            :disabled="botConnected"
          >
        </div>

        <div class="form-actions">
          <button v-if="!botConnected" @click="connectBot" class="btn-primary" :disabled="isConnecting">
            <span v-if="isConnecting" class="spinner"></span>
            {{ isConnecting ? 'Подключение...' : 'Подключить бота' }}
          </button>
          <button v-else @click="disconnectBot" class="btn-danger">
            Отключить бота
          </button>
        </div>
      </div>

      <div v-if="botConnected" class="bot-info">
        <div class="info-item">
          <span class="label">Имя бота:</span>
          <span class="value">{{ botInfo.name }}</span>
        </div>
        <div class="info-item">
          <span class="label">ID бота:</span>
          <span class="value">{{ botInfo.id }}</span>
        </div>
        <div class="info-item">
          <span class="label">Подключен:</span>
          <span class="value">{{ formatDate(botInfo.connected_at) }}</span>
        </div>
      </div>
    </div>

    <div class="settings-card">
      <div class="card-header">
        <h2>Настройки автопубликации</h2>
      </div>

      <div class="settings-form">
        <div class="form-section toggle-section">
          <div class="toggle-label">
            <span>Включить автопубликацию</span>
            <div class="tooltip-icon" @mouseenter="showTooltip = true" @mouseleave="showTooltip = false">
              <span>?</span>
              <div v-if="showTooltip" class="tooltip">
                При включении бот будет автоматически публиковать контент согласно расписанию
              </div>
            </div>
          </div>
          <label class="toggle">
            <input type="checkbox" v-model="autoPublishEnabled">
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div class="form-section">
          <label class="form-label">Часовой пояс</label>
          <select v-model="timezone" class="form-select">
            <option value="Europe/Moscow">Москва (UTC+3)</option>
            <option value="Europe/Kaliningrad">Калининград (UTC+2)</option>
            <option value="Asia/Yekaterinburg">Екатеринбург (UTC+5)</option>
            <option value="Asia/Novosibirsk">Новосибирск (UTC+7)</option>
            <option value="Asia/Vladivostok">Владивосток (UTC+10)</option>
          </select>
          <p class="help-text">
            Все запланированные публикации будут учитывать этот часовой пояс
          </p>
        </div>

        <div class="form-section">
          <label class="form-label">Интервал между публикациями (минимум)</label>
          <select v-model="minPostInterval" class="form-select">
            <option value="0">Без ограничений</option>
            <option value="5">5 минут</option>
            <option value="10">10 минут</option>
            <option value="15">15 минут</option>
            <option value="30">30 минут</option>
            <option value="60">1 час</option>
            <option value="120">2 часа</option>
          </select>
        </div>

        <div class="form-section toggle-section">
          <div class="toggle-label">
            <span>Добавлять подпись к постам</span>
          </div>
          <label class="toggle">
            <input type="checkbox" v-model="addSignature">
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div v-if="addSignature" class="form-section">
          <label class="form-label">Подпись к постам</label>
          <textarea
            v-model="postSignature"
            class="form-textarea"
            placeholder="Например: Подпишись на наш канал @channelname"
            rows="3"
          ></textarea>
          <p class="help-text">
            Эта подпись будет добавляться ко всем постам автоматически
          </p>
        </div>

        <div class="form-actions">
          <button @click="saveSettings" class="btn-primary">
            Сохранить настройки
          </button>
        </div>
      </div>
    </div>

    <div class="settings-card">
      <div class="card-header">
        <h2>Журнал автопубликаций</h2>
      </div>

      <div class="log-table">
        <table>
          <thead>
            <tr>
              <th>Дата</th>
              <th>Канал</th>
              <th>Пост</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="publishLogs.length === 0">
              <td colspan="4" class="empty-log">
                История публикаций пуста
              </td>
            </tr>
            <tr v-for="(log, index) in publishLogs" :key="index">
              <td>{{ formatDate(log.date) }}</td>
              <td>{{ log.channel }}</td>
              <td>{{ log.post }}</td>
              <td>
                <span :class="['status-badge', log.status]">
                  {{ getStatusText(log.status) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Состояние бота
const botConnected = ref(false)
const botToken = ref('')
const botUsername = ref('')
const isConnecting = ref(false)
const showToken = ref(false)
const botInfo = ref({
  id: '',
  name: '',
  connected_at: new Date()
})

// Настройки автопубликации
const autoPublishEnabled = ref(true)
const timezone = ref('Europe/Moscow')
const minPostInterval = ref('15')
const addSignature = ref(false)
const postSignature = ref('')
const showTooltip = ref(false)

// Журнал публикаций
const publishLogs = ref([
  {
    date: new Date(Date.now() - 24 * 60 * 60 * 1000),
    channel: '@spacebot',
    post: 'Поздравление с 8 марта',
    status: 'success'
  },
  {
    date: new Date(Date.now() - 48 * 60 * 60 * 1000),
    channel: '@spacebot',
    post: 'Обучение: как достичь звания Консультант',
    status: 'success'
  },
  {
    date: new Date(Date.now() - 72 * 60 * 60 * 1000),
    channel: '@spacebot',
    post: 'Релокация офиса в новый бизнес-центр',
    status: 'error'
  }
])

onMounted(() => {
  // Инициализация настроек из сохраненных данных
  loadBotSettings()
})

const loadBotSettings = () => {
  // В реальном приложении здесь бы загружались данные с сервера
  // Временно используем моки
  setTimeout(() => {
    botConnected.value = true
    botToken.value = '1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk'
    botUsername.value = '@webpub_test_bot'
    botInfo.value = {
      id: '123456789',
      name: 'WEBPUB Test Bot',
      connected_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
    }
  }, 500)
}

const connectBot = () => {
  if (!botToken.value || !botUsername.value) {
    alert('Пожалуйста, введите токен и username бота')
    return
  }

  isConnecting.value = true
  
  // Имитация подключения к API Telegram
  setTimeout(() => {
    botConnected.value = true
    isConnecting.value = false
    botInfo.value = {
      id: '123456789',
      name: 'WEBPUB Test Bot',
      connected_at: new Date()
    }
  }, 2000)
}

const disconnectBot = () => {
  const confirmed = confirm('Вы уверены, что хотите отключить бота? Это приведет к остановке всех автопубликаций.')
  if (confirmed) {
    botConnected.value = false
    botToken.value = ''
    botUsername.value = ''
  }
}

const saveSettings = () => {
  // В реальном приложении здесь был бы запрос к серверу
  alert('Настройки сохранены')
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString('ru-RU')
}

const getStatusText = (status) => {
  switch (status) {
    case 'success': return 'Опубликовано'
    case 'error': return 'Ошибка'
    case 'pending': return 'В очереди'
    default: return status
  }
}
</script>

<style scoped>
.bot-settings-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.settings-header {
  margin-bottom: 2rem;
}

.settings-header h1 {
  font-size: 1.8rem;
  margin: 0 0 0.5rem;
  color: #1a202c;
}

.subtitle {
  color: #4a5568;
  font-size: 1rem;
}

.settings-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
  overflow: hidden;
}

.card-header {
  padding: 1.25rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  font-size: 1.25rem;
  margin: 0;
  color: #2d3748;
}

.bot-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #718096;
}

.bot-status.connected {
  color: #38a169;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #e53e3e;
  display: inline-block;
}

.bot-status.connected .status-dot {
  background-color: #38a169;
}

.settings-form {
  padding: 1.5rem;
}

.form-section {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #2d3748;
}

.form-input, .form-select, .form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  border-color: #4299e1;
  outline: none;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.token-input {
  display: flex;
  align-items: center;
}

.token-input .form-input {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border-right: none;
}

.toggle-btn {
  background: #f7fafc;
  border: 1px solid #e2e8f0;
  border-left: none;
  border-top-right-radius: 6px;
  border-bottom-right-radius: 6px;
  padding: 0 1rem;
  height: 42px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.toggle-btn:hover {
  background: #edf2f7;
}

.help-text {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #718096;
}

.help-text a {
  color: #4299e1;
  text-decoration: none;
}

.help-text a:hover {
  text-decoration: underline;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-primary, .btn-danger {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: none;
}

.btn-primary {
  background-color: #4299e1;
  color: white;
}

.btn-primary:hover {
  background-color: #3182ce;
}

.btn-primary:disabled {
  background-color: #90cdf4;
  cursor: not-allowed;
}

.btn-danger {
  background-color: #f56565;
  color: white;
}

.btn-danger:hover {
  background-color: #e53e3e;
}

.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.bot-info {
  padding: 1rem 1.5rem;
  background-color: #f7fafc;
  border-top: 1px solid #e2e8f0;
}

.info-item {
  display: flex;
  margin-bottom: 0.5rem;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-item .label {
  font-weight: 500;
  color: #4a5568;
  width: 120px;
}

.info-item .value {
  color: #2d3748;
}

.toggle-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #2d3748;
  font-weight: 500;
}

.tooltip-icon {
  position: relative;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background-color: #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  color: #4a5568;
  cursor: pointer;
}

.tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 8px;
  width: 250px;
  padding: 0.5rem;
  background-color: #2d3748;
  color: white;
  font-size: 0.75rem;
  border-radius: 4px;
  z-index: 10;
  font-weight: normal;
}

.tooltip:after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-width: 5px;
  border-style: solid;
  border-color: #2d3748 transparent transparent transparent;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #cbd5e0;
  transition: .4s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: #4299e1;
}

input:checked + .toggle-slider:before {
  transform: translateX(24px);
}

.log-table {
  padding: 1rem;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 0.75rem;
  border-bottom: 2px solid #e2e8f0;
  color: #4a5568;
  font-weight: 600;
}

td {
  padding: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
  color: #2d3748;
}

.empty-log {
  text-align: center;
  color: #a0aec0;
  padding: 2rem 0;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.success {
  background-color: #c6f6d5;
  color: #22543d;
}

.status-badge.error {
  background-color: #fed7d7;
  color: #822727;
}

.status-badge.pending {
  background-color: #e9ecef;
  color: #4a5568;
}

@media (max-width: 640px) {
  .bot-settings-view {
    padding: 1rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn-primary, .btn-danger {
    width: 100%;
    justify-content: center;
  }
}
</style> 