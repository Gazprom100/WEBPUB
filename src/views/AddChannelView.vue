<template>
  <div class="add-channel-view">
    <div class="content-card">
      <div class="card-header">
        <h1>Add New Channel</h1>
        <p class="subtitle">Connect your Telegram channel to start managing and monetizing</p>
      </div>

      <form @submit.prevent="handleSubmit" class="channel-form">
        <div class="form-section">
          <h2>Channel Information</h2>
          
          <div class="form-group">
            <label class="form-label">Channel Username or Link</label>
            <div class="input-group">
              <span class="input-prefix">@</span>
              <input 
                type="text" 
                v-model="channelUsername"
                class="form-input"
                :class="{ 'error': errors.channelUsername }"
                placeholder="yourchannel"
                required
              >
            </div>
            <span v-if="errors.channelUsername" class="error-text">{{ errors.channelUsername }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">Category</label>
            <select v-model="category" class="form-input" required>
              <option value="">Select category</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
            <span v-if="errors.category" class="error-text">{{ errors.category }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">Description</label>
            <textarea 
              v-model="description"
              class="form-input"
              :class="{ 'error': errors.description }"
              rows="4"
              placeholder="Tell us about your channel..."
            ></textarea>
            <span v-if="errors.description" class="error-text">{{ errors.description }}</span>
          </div>
        </div>

        <div class="form-section">
          <h2>Monetization Settings</h2>
          
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="enableMonetization">
              Enable monetization for this channel
            </label>
          </div>

          <div v-if="enableMonetization" class="monetization-options">
            <div class="form-group">
              <label class="form-label">Minimum Post Price</label>
              <div class="input-group">
                <span class="input-prefix">$</span>
                <input 
                  type="number" 
                  v-model="minPostPrice"
                  class="form-input"
                  min="0"
                  step="0.01"
                >
              </div>
            </div>

            <div class="form-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="allowNegotiation">
                Allow price negotiation
              </label>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn btn-secondary" @click="$router.back()">
            Cancel
          </button>
          <button type="submit" class="btn btn-primary" :disabled="isLoading">
            {{ isLoading ? 'Connecting...' : 'Connect Channel' }}
          </button>
        </div>

        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const channelUsername = ref('')
const category = ref('')
const description = ref('')
const enableMonetization = ref(false)
const minPostPrice = ref(100)
const allowNegotiation = ref(true)
const isLoading = ref(false)
const error = ref('')

const errors = reactive({
  channelUsername: '',
  category: '',
  description: ''
})

const categories = [
  { id: 'news', name: 'News & Media' },
  { id: 'entertainment', name: 'Entertainment' },
  { id: 'business', name: 'Business & Finance' },
  { id: 'technology', name: 'Technology' },
  { id: 'education', name: 'Education' },
  { id: 'lifestyle', name: 'Lifestyle' },
  { id: 'other', name: 'Other' }
]

const validateForm = () => {
  let isValid = true
  errors.channelUsername = ''
  errors.category = ''
  errors.description = ''

  if (!channelUsername.value) {
    errors.channelUsername = 'Channel username is required'
    isValid = false
  }

  if (!category.value) {
    errors.category = 'Please select a category'
    isValid = false
  }

  if (description.value && description.value.length > 500) {
    errors.description = 'Description must be less than 500 characters'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  error.value = ''

  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/channels`, {
      username: channelUsername.value,
      category: category.value,
      description: description.value,
      monetization: enableMonetization.value ? {
        enabled: true,
        minPostPrice: minPostPrice.value,
        allowNegotiation: allowNegotiation.value
      } : {
        enabled: false
      }
    })

    router.push(`/channels/${response.data.id}`)
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to connect channel'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.add-channel-view {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.content-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.card-header {
  text-align: center;
  margin-bottom: 2rem;
}

h1 {
  font-size: 1.8rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--text-color);
  opacity: 0.8;
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border-color);
}

.form-section h2 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.input-group {
  display: flex;
  align-items: center;
}

.input-prefix {
  background: var(--background-color);
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-right: none;
  border-radius: 4px 0 0 4px;
  color: var(--text-color);
}

.input-group .form-input {
  border-radius: 0 4px 4px 0;
}

.monetization-options {
  margin-top: 1rem;
  padding: 1rem;
  background: var(--background-color);
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.alert {
  margin-top: 1rem;
}
</style> 