<template>
  <div class="create-post">
    <div class="page-header">
      <h1>Создать новый пост</h1>
    </div>

    <div class="post-form-container">
      <form @submit.prevent="handleSubmit" class="post-form">
        <div class="form-group">
          <label>Выберите канал</label>
          <select v-model="selectedChannel" class="form-input" required>
            <option value="">Выберите канал</option>
            <option v-for="channel in channels" :key="channel.id" :value="channel.id">
              {{ channel.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Заголовок</label>
          <input 
            type="text" 
            v-model="title" 
            class="form-input"
            placeholder="Введите заголовок поста"
            required
          >
        </div>

        <div class="form-group">
          <label>Описание</label>
          <textarea 
            v-model="description" 
            class="form-input"
            rows="4"
            placeholder="Введите описание поста"
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label>Тип контента</label>
          <select v-model="contentType" class="form-input" required>
            <option value="text">Текст</option>
            <option value="video">Видео</option>
            <option value="image">Изображение</option>
            <option value="link">Ссылка</option>
          </select>
        </div>

        <div class="form-group" v-if="contentType === 'text'">
          <label>Текст поста</label>
          <textarea 
            v-model="content" 
            class="form-input"
            rows="8"
            placeholder="Введите текст поста"
            required
          ></textarea>
        </div>

        <div class="form-group" v-if="contentType === 'video' || contentType === 'image'">
          <label>URL медиа</label>
          <input 
            type="url" 
            v-model="content"
            class="form-input"
            :placeholder="contentType === 'video' ? 'Введите URL видео' : 'Введите URL изображения'"
            required
          >
        </div>

        <div class="form-group" v-if="contentType === 'link'">
          <label>URL</label>
          <input 
            type="url" 
            v-model="content"
            class="form-input"
            placeholder="Введите URL"
            required
          >
        </div>

        <div class="form-group">
          <label>Теги</label>
          <div class="tags-input">
            <input 
              type="text" 
              v-model="tagInput"
              @keydown.enter.prevent="addTag"
              class="form-input"
              placeholder="Добавьте теги и нажмите Enter"
            >
            <div class="tags-list" v-if="tags.length">
              <span v-for="(tag, index) in tags" :key="index" class="tag">
                {{ tag }}
                <button type="button" @click="removeTag(index)" class="tag-remove">&times;</button>
              </span>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="isScheduled">
            Запланировать публикацию
          </label>
        </div>

        <div class="form-group" v-if="isScheduled">
          <label>Дата и время публикации</label>
          <input 
            type="datetime-local" 
            v-model="scheduledDate"
            class="form-input"
            :min="minDateTime"
            required
          >
        </div>

        <div class="form-actions">
          <button type="button" class="btn btn-secondary" @click="$router.back()">
            Отмена
          </button>
          <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
            {{ isSubmitting ? 'Создание...' : 'Создать пост' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useChannelsStore } from '@/stores/channels'
import axios from 'axios'

const router = useRouter()
const channelsStore = useChannelsStore()

// Form data
const selectedChannel = ref('')
const title = ref('')
const description = ref('')
const contentType = ref('text')
const content = ref('')
const tagInput = ref('')
const tags = ref([])
const isScheduled = ref(false)
const scheduledDate = ref('')
const isSubmitting = ref(false)

// Computed
const channels = computed(() => channelsStore.channels)
const minDateTime = computed(() => {
  const now = new Date()
  now.setMinutes(now.getMinutes() + 5) // Минимум 5 минут от текущего времени
  return now.toISOString().slice(0, 16)
})

// Methods
const addTag = () => {
  const tag = tagInput.value.trim()
  if (tag && !tags.value.includes(tag)) {
    tags.value.push(tag)
    tagInput.value = ''
  }
}

const removeTag = (index) => {
  tags.value.splice(index, 1)
}

const handleSubmit = async () => {
  if (isSubmitting.value) return

  isSubmitting.value = true
  try {
    const postData = {
      channelId: selectedChannel.value,
      title: title.value,
      description: description.value,
      contentType: contentType.value,
      content: content.value,
      tags: tags.value,
      scheduledAt: isScheduled.value ? new Date(scheduledDate.value).toISOString() : null
    }

    const response = await axios.post(`${import.meta.env.VITE_API_URL}/posts`, postData)
    router.push(`/channels/${selectedChannel.value}/posts/${response.data.id}`)
  } catch (error) {
    console.error('Ошибка при создании поста:', error)
    // Здесь можно добавить обработку ошибок и показ уведомлений
  } finally {
    isSubmitting.value = false
  }
}

// Загружаем список каналов при монтировании компонента
channelsStore.fetchChannels()
</script>

<style scoped>
.create-post {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  margin-bottom: 2rem;
}

.post-form-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
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

.form-input:focus {
  border-color: var(--primary-color);
  outline: none;
}

.tags-input {
  margin-top: 0.5rem;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  background: var(--background-color);
  border-radius: 4px;
  font-size: 0.9rem;
}

.tag-remove {
  margin-left: 0.5rem;
  border: none;
  background: none;
  color: var(--text-color);
  cursor: pointer;
  padding: 0 0.25rem;
}

.tag-remove:hover {
  color: var(--error-color);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
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

.btn-primary:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-secondary {
  background: var(--background-color);
  color: var(--text-color);
}

.btn-secondary:hover {
  background: var(--border-color);
}
</style> 