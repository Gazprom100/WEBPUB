<template>
  <div class="forgot-password-view">
    <div class="forgot-password-container">
      <div class="forgot-password-header">
        <h1>Forgot Password</h1>
        <p>Enter your email address and we'll send you instructions to reset your password</p>
      </div>

      <form @submit.prevent="handleSubmit" class="forgot-password-form">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            type="email"
            id="email"
            v-model="form.email"
            required
            placeholder="Enter your email"
            :class="{ 'error': errors.email }"
          />
          <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
        </div>

        <button type="submit" class="btn btn-primary" :disabled="isLoading">
          <span v-if="isLoading" class="spinner"></span>
          {{ isLoading ? 'Sending Instructions...' : 'Send Reset Instructions' }}
        </button>

        <div class="form-footer">
          <p>Remember your password? <router-link to="/login">Sign in</router-link></p>
        </div>
      </form>

      <div v-if="success" class="success-message">
        <i class="fas fa-check-circle"></i>
        <h3>Instructions Sent</h3>
        <p>We've sent password reset instructions to your email address. Please check your inbox.</p>
        <button class="btn btn-outline" @click="resetForm">Back to Login</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const isLoading = ref(false)
const success = ref(false)

const form = reactive({
  email: ''
})

const errors = reactive({
  email: ''
})

const validateForm = () => {
  let isValid = true
  errors.email = ''

  if (!form.email.trim()) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Please enter a valid email'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  try {
    await axios.post('/api/auth/forgot-password', {
      email: form.email
    })
    success.value = true
  } catch (error) {
    if (error.response?.data?.message) {
      errors.email = error.response.data.message
    } else {
      errors.email = 'An error occurred. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}

const resetForm = () => {
  form.email = ''
  success.value = false
  router.push('/login')
}
</script>

<style scoped>
.forgot-password-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%);
  padding: 2rem;
}

.forgot-password-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 480px;
  padding: 2.5rem;
  animation: fadeIn 0.5s ease-out;
}

.forgot-password-header {
  text-align: center;
  margin-bottom: 2rem;
}

.forgot-password-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 0.5rem;
}

.forgot-password-header p {
  color: #4a5568;
  margin: 0;
  font-size: 1rem;
}

.forgot-password-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2d3748;
  font-size: 0.95rem;
}

.form-group input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: #f8fafc;
}

.form-group input:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.15);
  background: white;
}

.form-group input.error {
  border-color: #e53e3e;
}

.error-message {
  color: #e53e3e;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  display: block;
}

.btn {
  padding: 0.875rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
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

.btn-outline {
  background: transparent;
  border: 2px solid #4299e1;
  color: #4299e1;
}

.btn-outline:hover:not(:disabled) {
  background: #4299e1;
  color: white;
}

.spinner {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

.form-footer {
  text-align: center;
  margin-top: 1rem;
  color: #4a5568;
}

.form-footer a {
  color: #4299e1;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.form-footer a:hover {
  color: #3182ce;
}

.success-message {
  text-align: center;
  padding: 2rem;
  animation: fadeIn 0.5s ease-out;
}

.success-message i {
  font-size: 3rem;
  color: #48bb78;
  margin-bottom: 1rem;
}

.success-message h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 0.5rem;
}

.success-message p {
  color: #4a5568;
  margin: 0 0 1.5rem;
  font-size: 1rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 640px) {
  .forgot-password-container {
    padding: 2rem;
  }
  
  .forgot-password-header h1 {
    font-size: 1.75rem;
  }
}
</style> 