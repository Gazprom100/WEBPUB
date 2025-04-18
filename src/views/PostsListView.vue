<template>
  <div class="posts-list-view">
    <div class="posts-header">
      <h1>Посты</h1>
      <div class="posts-actions">
        <button class="btn btn-primary" @click="$router.push('/posts/create')">
          Создать пост
        </button>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="filters-section">
      <div class="search-box">
        <input 
          type="text" 
          v-model="filters.searchQuery"
          placeholder="Поиск постов..."
          @input="handleSearch"
        >
      </div>

      <div class="filter-group">
        <select v-model="filters.channelId" @change="handleFiltersChange">
          <option value="">Все каналы</option>
          <option v-for="channel in channels" :key="channel.id" :value="channel.id">
            {{ channel.name }}
          </option>
        </select>

        <select v-model="filters.status" @change="handleFiltersChange">
          <option value="">Все статусы</option>
          <option value="draft">Черновики</option>
          <option value="scheduled">Запланированные</option>
          <option value="published">Опубликованные</option>
        </select>

        <select v-model="filters.sortBy" @change="handleFiltersChange">
          <option value="created_at">По дате создания</option>
          <option value="scheduled_at">По дате публикации</option>
          <option value="views">По просмотрам</option>
          <option value="engagement">По вовлеченности</option>
        </select>
      </div>
    </div>

    <!-- Список постов -->
    <div class="posts-grid" v-if="!loading && posts.length">
      <div v-for="post in posts" :key="post.id" class="post-card">
        <div class="post-preview" :class="{ 'has-thumbnail': post.thumbnail }">
          <img v-if="post.thumbnail" :src="post.thumbnail" :alt="post.title">
          <div v-else class="no-thumbnail">
            <i class="fas fa-file-alt"></i>
          </div>
        </div>

        <div class="post-content">
          <div class="post-header">
            <h3 class="post-title">{{ post.title }}</h3>
            <span class="post-status" :class="post.status">
              {{ getStatusLabel(post.status) }}
            </span>
          </div>

          <p class="post-description">{{ post.description }}</p>

          <div class="post-meta">
            <div class="meta-item">
              <i class="fas fa-eye"></i>
              {{ formatNumber(post.views) }}
            </div>
            <div class="meta-item">
              <i class="fas fa-thumbs-up"></i>
              {{ formatNumber(post.likes) }}
            </div>
            <div class="meta-item">
              <i class="fas fa-comment"></i>
              {{ formatNumber(post.comments) }}
            </div>
            <div class="meta-item">
              <i class="fas fa-share"></i>
              {{ formatNumber(post.shares) }}
            </div>
          </div>

          <div class="post-footer">
            <span class="post-date">
              {{ formatDate(post.created_at) }}
            </span>
            <div class="post-actions">
              <button class="btn btn-icon" @click="editPost(post)">
                <i class="fas fa-edit"></i>
              </button>
              <button class="btn btn-icon" @click="deletePost(post)">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Состояние загрузки -->
    <div v-else-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка постов...</p>
    </div>

    <!-- Пустое состояние -->
    <div v-else class="empty-state">
      <i class="fas fa-file-alt"></i>
      <h2>Нет постов</h2>
      <p>Создайте свой первый пост, чтобы начать публикацию контента</p>
      <button class="btn btn-primary" @click="$router.push('/posts/create')">
        Создать пост
      </button>
    </div>

    <!-- Пагинация -->
    <div class="pagination" v-if="totalPages > 1">
      <button 
        class="btn btn-secondary" 
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        Назад
      </button>
      
      <span class="page-info">
        Страница {{ currentPage }} из {{ totalPages }}
      </span>
      
      <button 
        class="btn btn-secondary" 
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        Вперед
      </button>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <div class="modal" v-if="showDeleteModal">
      <div class="modal-content">
        <h2>Удалить пост?</h2>
        <p>Вы уверены, что хотите удалить пост "{{ postToDelete?.title }}"?</p>
        <p>Это действие нельзя отменить.</p>
        
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="cancelDelete">
            Отмена
          </button>
          <button class="btn btn-danger" @click="confirmDelete">
            Удалить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePostsStore } from '@/stores/posts'
import { useChannelsStore } from '@/stores/channels'
import { debounce } from 'lodash'

const router = useRouter()
const postsStore = usePostsStore()
const channelsStore = useChannelsStore()

// Состояния
const loading = ref(false)
const posts = ref([])
const channels = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const showDeleteModal = ref(false)
const postToDelete = ref(null)

const filters = reactive({
  channelId: '',
  status: '',
  sortBy: 'created_at',
  searchQuery: ''
})

// Методы
const fetchPosts = async () => {
  loading.value = true
  try {
    const response = await postsStore.fetchPosts({
      page: currentPage.value,
      ...filters
    })
    posts.value = response.posts
    totalPages.value = response.totalPages
  } catch (error) {
    console.error('Ошибка при загрузке постов:', error)
  } finally {
    loading.value = false
  }
}

const fetchChannels = async () => {
  try {
    const response = await channelsStore.fetchChannels()
    channels.value = response
  } catch (error) {
    console.error('Ошибка при загрузке каналов:', error)
  }
}

const handleSearch = debounce(() => {
  currentPage.value = 1
  fetchPosts()
}, 300)

const handleFiltersChange = () => {
  currentPage.value = 1
  fetchPosts()
}

const changePage = (page) => {
  currentPage.value = page
  fetchPosts()
}

const editPost = (post) => {
  router.push(`/posts/${post.id}/edit`)
}

const deletePost = (post) => {
  postToDelete.value = post
  showDeleteModal.value = true
}

const cancelDelete = () => {
  postToDelete.value = null
  showDeleteModal.value = false
}

const confirmDelete = async () => {
  try {
    await postsStore.deletePost(postToDelete.value.id)
    showDeleteModal.value = false
    postToDelete.value = null
    fetchPosts()
  } catch (error) {
    console.error('Ошибка при удалении поста:', error)
  }
}

const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const getStatusLabel = (status) => {
  const labels = {
    draft: 'Черновик',
    scheduled: 'Запланирован',
    published: 'Опубликован'
  }
  return labels[status] || status
}

// Загрузка данных
onMounted(() => {
  fetchChannels()
  fetchPosts()
})
</script>

<style scoped>
.posts-list-view {
  padding: 2rem;
}

.posts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.filters-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-box {
  margin-bottom: 1rem;
}

.search-box input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
}

.filter-group {
  display: flex;
  gap: 1rem;
}

.filter-group select {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
  background: white;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.post-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.post-card:hover {
  transform: translateY(-4px);
}

.post-preview {
  height: 200px;
  background: var(--background-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.post-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-thumbnail {
  font-size: 3rem;
  color: var(--text-color);
  opacity: 0.3;
}

.post-content {
  padding: 1.5rem;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.post-title {
  margin: 0;
  font-size: 1.25rem;
  line-height: 1.4;
}

.post-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
}

.post-status.draft {
  background: var(--warning-color-light);
  color: var(--warning-color);
}

.post-status.scheduled {
  background: var(--info-color-light);
  color: var(--info-color);
}

.post-status.published {
  background: var(--success-color-light);
  color: var(--success-color);
}

.post-description {
  margin: 0 0 1rem;
  font-size: 0.875rem;
  color: var(--text-color);
  opacity: 0.7;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-color);
  opacity: 0.7;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-date {
  font-size: 0.875rem;
  color: var(--text-color);
  opacity: 0.7;
}

.post-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  padding: 0.5rem;
  font-size: 1rem;
  background: none;
  border: none;
  color: var(--text-color);
  opacity: 0.7;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover {
  opacity: 1;
  color: var(--primary-color);
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading-state .spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  margin: 0 auto 1rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state i {
  font-size: 4rem;
  color: var(--text-color);
  opacity: 0.3;
  margin-bottom: 1rem;
}

.empty-state h2 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
}

.empty-state p {
  margin: 0 0 1.5rem;
  color: var(--text-color);
  opacity: 0.7;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-info {
  font-size: 0.875rem;
  color: var(--text-color);
  opacity: 0.7;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 400px;
  width: 100%;
}

.modal-content h2 {
  margin: 0 0 1rem;
}

.modal-content p {
  margin: 0 0 1.5rem;
  color: var(--text-color);
  opacity: 0.7;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style> 