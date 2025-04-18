<template>
  <div class="login-view">
    <div class="auth-card">
      <h1>Добро пожаловать</h1>
      <p class="subtitle">Войдите для управления каналами</p>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <div class="form-group">
          <label class="form-label">Email</label>
          <input 
            type="email" 
            v-model="email" 
            class="form-input"
            :class="{ 'error': errors.email }"
            placeholder="your@email.com"
            required
            autocomplete="email"
          >
          <span v-if="errors.email" class="error-text">{{ errors.email }}</span>
        </div>

        <div class="form-group">
          <label class="form-label">Пароль</label>
          <div class="password-input">
            <input 
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              class="form-input"
              :class="{ 'error': errors.password }"
              placeholder="••••••••"
              required
              autocomplete="current-password"
            >
            <button 
              type="button" 
              class="password-toggle" 
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? '🙈' : '👁️' }}
            </button>
          </div>
          <span v-if="errors.password" class="error-text">{{ errors.password }}</span>
        </div>

        <div class="form-actions">
          <label class="checkbox-label">
            <input 
              type="checkbox" 
              v-model="rememberMe"
              class="checkbox-input"
            >
            <span class="checkbox-text">Запомнить меня</span>
          </label>
          <router-link to="/forgot-password" class="forgot-link">
            Забыли пароль?
          </router-link>
        </div>

        <button 
          type="submit" 
          class="btn btn-primary btn-block" 
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? 'Вход...' : 'Войти' }}
        </button>

        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>
      </form>

      <div class="auth-footer">
        <p>
          Нет аккаунта? 
          <router-link to="/signup" class="signup-link">
            Зарегистрироваться
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const isLoading = ref(false)
const error = ref('')
const showPassword = ref(false)
const errors = reactive({
  email: '',
  password: ''
})

// Восстанавливаем email из localStorage, если пользователь ранее выбрал "Запомнить меня"
onMounted(() => {
  const savedEmail = localStorage.getItem('remember_email')
  if (savedEmail) {
    email.value = savedEmail
    rememberMe.value = true
  }
})

const validateForm = () => {
  let isValid = true
  errors.email = ''
  errors.password = ''

  // Валидация email
  if (!email.value) {
    errors.email = 'Email обязателен'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.email = 'Введите корректный email'
    isValid = false
  }

  // Валидация пароля
  if (!password.value) {
    errors.password = 'Пароль обязателен'
    isValid = false
  } else if (password.value.length < 6) {
    errors.password = 'Пароль должен быть не менее 6 символов'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  error.value = ''

  try {
    await auth.login(email.value, password.value, rememberMe.value)
    
    if (rememberMe.value) {
      localStorage.setItem('remember_email', email.value)
    } else {
      localStorage.removeItem('remember_email')
    }

    // Редирект на сохраненный маршрут или на страницу каналов
    const redirectPath = route.query.redirect || '/channels'
    router.push(redirectPath)
  } catch (err) {
    if (err.response?.status === 401) {
      error.value = 'Неверный email или пароль'
    } else if (err.response?.status === 429) {
      error.value = 'Слишком много попыток входа. Попробуйте позже'
    } else {
      error.value = 'Ошибка при входе в систему'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: var(--background-color);
}

.auth-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2.5rem;
  width: 100%;
  max-width: 420px;
}

h1 {
  font-size: 2rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  color: var(--text-color);
  opacity: 0.8;
  text-align: center;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color);
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1.5px solid var(--border-color);
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.2s;
}

.form-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.1);
  outline: none;
}

.form-input.error {
  border-color: var(--error-color);
}

.error-text {
  color: var(--error-color);
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.password-input {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  font-size: 1.25rem;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-input {
  width: 1.125rem;
  height: 1.125rem;
}

.checkbox-text {
  font-size: 0.875rem;
  color: var(--text-color);
}

.forgot-link {
  color: var(--primary-color);
  text-decoration: none;
  font-size: 0.875rem;
  transition: opacity 0.2s;
}

.forgot-link:hover {
  opacity: 0.8;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.875rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
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

.loading-spinner {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.alert {
  padding: 1rem;
  border-radius: 6px;
  margin-top: 1rem;
  font-size: 0.875rem;
}

.alert-error {
  background: var(--error-bg-color);
  color: var(--error-color);
  border: 1px solid var(--error-border-color);
}

.auth-footer {
  text-align: center;
  margin-top: 2rem;
  color: var(--text-color);
  font-size: 0.875rem;
}

.signup-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
}

.signup-link:hover {
  text-decoration: underline;
}
</style> 