<template>
  <div class="post-editor-view">
    <header class="header">
      <h1>{{ isEditing ? 'Edit Post' : 'Create New Post' }}</h1>
      <div class="actions">
        <button class="btn btn-outline" @click="saveDraft">Save Draft</button>
        <button class="btn btn-primary" @click="publish">Publish</button>
      </div>
    </header>

    <div class="editor-container">
      <form @submit.prevent="handleSubmit" class="editor-form">
        <div class="form-group">
          <label for="channel">Channel</label>
          <select v-model="form.channelId" id="channel" required>
            <option value="">Select Channel</option>
            <option v-for="channel in channels" :key="channel.id" :value="channel.id">
              {{ channel.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="title">Title</label>
          <input
            type="text"
            id="title"
            v-model="form.title"
            required
            placeholder="Enter post title"
            maxlength="100"
          />
          <span class="character-count">{{ form.title.length }}/100</span>
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea
            id="description"
            v-model="form.description"
            rows="3"
            placeholder="Enter post description"
            maxlength="500"
          ></textarea>
          <span class="character-count">{{ form.description.length }}/500</span>
        </div>

        <div class="form-group">
          <label>Content</label>
          <div class="content-editor">
            <div class="toolbar">
              <button type="button" @click="addImage">
                <i class="fas fa-image"></i> Add Image
              </button>
              <button type="button" @click="addVideo">
                <i class="fas fa-video"></i> Add Video
              </button>
              <button type="button" @click="addLink">
                <i class="fas fa-link"></i> Add Link
              </button>
            </div>
            <textarea
              v-model="form.content"
              rows="10"
              placeholder="Write your post content here..."
            ></textarea>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="schedule">Schedule Post</label>
            <input
              type="datetime-local"
              id="schedule"
              v-model="form.scheduledAt"
              :min="minScheduleDate"
            />
          </div>

          <div class="form-group">
            <label for="tags">Tags</label>
            <input
              type="text"
              id="tags"
              v-model="tagInput"
              @keydown.enter.prevent="addTag"
              placeholder="Add tags (press Enter)"
            />
            <div class="tags-container">
              <span v-for="(tag, index) in form.tags" :key="index" class="tag">
                {{ tag }}
                <button type="button" @click="removeTag(index)">&times;</button>
              </span>
            </div>
          </div>
        </div>

        <div class="form-group settings">
          <h3>Post Settings</h3>
          <div class="settings-grid">
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.settings.allowComments" />
              Allow Comments
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.settings.isMonetized" />
              Enable Monetization
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.settings.isAgeRestricted" />
              Age Restriction
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.settings.isPrivate" />
              Private Post
            </label>
          </div>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>

      <div class="preview-panel">
        <h3>Preview</h3>
        <div class="preview-content">
          <h2>{{ form.title || 'Post Title' }}</h2>
          <p class="description">{{ form.description || 'Post description will appear here...' }}</p>
          <div class="content-preview" v-html="formattedContent"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const isEditing = computed(() => !!route.params.id)

const channels = ref([])
const error = ref('')
const tagInput = ref('')

const form = ref({
  channelId: '',
  title: '',
  description: '',
  content: '',
  scheduledAt: '',
  tags: [],
  settings: {
    allowComments: true,
    isMonetized: false,
    isAgeRestricted: false,
    isPrivate: false
  }
})

const minScheduleDate = computed(() => {
  const now = new Date()
  return now.toISOString().slice(0, 16)
})

const formattedContent = computed(() => {
  // Here you would implement content formatting/preview
  return form.value.content
})

onMounted(async () => {
  try {
    // Fetch channels
    const response = await axios.get('/api/channels')
    channels.value = response.data

    if (isEditing.value) {
      // Fetch post data if editing
      const postResponse = await axios.get(`/api/posts/${route.params.id}`)
      const post = postResponse.data
      form.value = {
        ...form.value,
        ...post,
        scheduledAt: post.scheduledAt ? new Date(post.scheduledAt).toISOString().slice(0, 16) : ''
      }
    }
  } catch (err) {
    error.value = 'Failed to load data. Please try again.'
  }
})

const addTag = () => {
  const tag = tagInput.value.trim()
  if (tag && !form.value.tags.includes(tag)) {
    form.value.tags.push(tag)
  }
  tagInput.value = ''
}

const removeTag = (index) => {
  form.value.tags.splice(index, 1)
}

const addImage = () => {
  // Implement image upload logic
}

const addVideo = () => {
  // Implement video upload logic
}

const addLink = () => {
  const url = prompt('Enter URL:')
  if (url) {
    form.value.content += `\n[Link](${url})\n`
  }
}

const saveDraft = async () => {
  try {
    const payload = { ...form.value, status: 'draft' }
    await savePost(payload)
    router.push('/posts')
  } catch (err) {
    error.value = 'Failed to save draft. Please try again.'
  }
}

const publish = async () => {
  try {
    const payload = { ...form.value, status: 'published' }
    await savePost(payload)
    router.push('/posts')
  } catch (err) {
    error.value = 'Failed to publish post. Please try again.'
  }
}

const savePost = async (payload) => {
  const url = isEditing.value ? `/api/posts/${route.params.id}` : '/api/posts'
  const method = isEditing.value ? 'put' : 'post'
  await axios[method](url, payload)
}

const handleSubmit = async () => {
  error.value = ''
  try {
    await savePost(form.value)
    router.push('/posts')
  } catch (err) {
    error.value = 'Failed to save post. Please try again.'
  }
}
</script>

<style scoped>
.post-editor-view {
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
  background: #f8f9fa;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.header h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 600;
  color: #1a1a1a;
}

.actions {
  display: flex;
  gap: 1rem;
}

.editor-container {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 2rem;
}

.editor-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.editor-form:hover {
  transform: translateY(-2px);
}

.form-group {
  margin-bottom: 1.5rem;
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 500;
  color: #2d3748;
  font-size: 0.95rem;
}

.form-group input[type="text"],
.form-group input[type="datetime-local"],
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: #f8fafc;
}

.form-group input[type="text"]:focus,
.form-group input[type="datetime-local"]:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.15);
  background: white;
}

.character-count {
  display: block;
  text-align: right;
  font-size: 0.75rem;
  color: #718096;
  margin-top: 0.25rem;
}

.content-editor {
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.content-editor:focus-within {
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.15);
}

.toolbar {
  padding: 0.75rem;
  border-bottom: 2px solid #e2e8f0;
  display: flex;
  gap: 0.75rem;
  background: #f8fafc;
}

.toolbar button {
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  color: #4a5568;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.toolbar button:hover {
  background: #edf2f7;
  border-color: #cbd5e0;
  color: #2d3748;
}

.toolbar button i {
  font-size: 1rem;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.tag {
  background: #edf2f7;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #2d3748;
  transition: all 0.2s ease;
}

.tag:hover {
  background: #e2e8f0;
}

.tag button {
  border: none;
  background: none;
  padding: 0;
  cursor: pointer;
  color: #718096;
  font-size: 1.25rem;
  line-height: 1;
  transition: color 0.2s ease;
}

.tag button:hover {
  color: #e53e3e;
}

.settings {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #e2e8f0;
}

.settings h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #2d3748;
  font-size: 1.1rem;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.checkbox-label:hover {
  background: #edf2f7;
}

.checkbox-label input[type="checkbox"] {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid #cbd5e0;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.checkbox-label input[type="checkbox"]:checked {
  background: #4299e1;
  border-color: #4299e1;
}

.preview-panel {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 2rem;
  transition: transform 0.2s ease;
}

.preview-panel:hover {
  transform: translateY(-2px);
}

.preview-panel h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e2e8f0;
  color: #2d3748;
  font-size: 1.25rem;
}

.preview-content {
  color: #2d3748;
}

.preview-content h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.preview-content .description {
  color: #4a5568;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.error-message {
  color: #e53e3e;
  margin-top: 1rem;
  padding: 1rem;
  background: #fff5f5;
  border-radius: 8px;
  border: 1px solid #fed7d7;
  font-size: 0.875rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.95rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-outline {
  background: transparent;
  border: 2px solid #4299e1;
  color: #4299e1;
}

.btn-outline:hover:not(:disabled) {
  background: #4299e1;
  color: white;
}

.btn-primary {
  background: #4299e1;
  border: 2px solid #4299e1;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #3182ce;
  border-color: #3182ce;
}

/* Анимации */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.editor-form,
.preview-panel {
  animation: fadeIn 0.3s ease-out;
}

/* Адаптивность */
@media (max-width: 1200px) {
  .editor-container {
    grid-template-columns: 1fr;
  }
  
  .preview-panel {
    position: static;
    margin-top: 2rem;
  }
}

@media (max-width: 768px) {
  .post-editor-view {
    padding: 1rem;
  }
  
  .header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .actions {
    width: 100%;
    justify-content: center;
  }
  
  .settings-grid {
    grid-template-columns: 1fr;
  }
}
</style> 