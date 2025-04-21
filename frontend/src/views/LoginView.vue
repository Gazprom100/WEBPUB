<template>
  <div class="login-container">
    <div class="login-box">
      <h1>Welcome to WEBPUB</h1>
      <p>You are automatically logged in as a test user</p>
      <router-link to="/dashboard" class="btn-primary">
        Go to Dashboard
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(async () => {
  // Автоматически входим как тестовый пользователь
  await authStore.login('test@example.com', 'password')
  router.push('/dashboard')
})
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
}

.login-box {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  max-width: 400px;
  width: 100%;
}

h1 {
  color: #fff;
  margin-bottom: 1rem;
}

p {
  color: #ccc;
  margin-bottom: 2rem;
}

.btn-primary {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 0.5rem;
  transition: background 0.3s;
}

.btn-primary:hover {
  background: #45a049;
}
</style> 