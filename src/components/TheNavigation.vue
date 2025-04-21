<template>
  <nav class="navigation">
    <div class="nav-left">
      <router-link to="/" class="logo">
        WEBPUB
      </router-link>
      <div class="nav-links">
        <router-link to="/channels">Каналы</router-link>
        <router-link to="/analytics">Аналитика</router-link>
        <router-link to="/monetization">Монетизация</router-link>
      </div>
    </div>
    <div class="nav-right">
      <div class="user-menu" v-if="isAuthenticated">
        <button class="notifications" @click="toggleNotifications">
          <span class="icon">🔔</span>
          <span v-if="unreadNotifications" class="badge">{{ unreadNotifications }}</span>
        </button>
        <div class="user-profile" @click="toggleUserMenu">
          <img :src="userAvatar" :alt="userName" class="avatar">
          <span class="user-name">{{ userName }}</span>
        </div>
      </div>
      <div v-else class="auth-buttons">
        <router-link to="/login" class="btn btn-login">Войти</router-link>
        <router-link to="/signup" class="btn btn-signup">Регистрация</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const isAuthenticated = computed(() => auth.isAuthenticated)
const userName = computed(() => auth.user?.name || '')
const userAvatar = computed(() => auth.user?.avatar || '/default-avatar.png')
const unreadNotifications = ref(2)

const toggleNotifications = () => {
  // Toggle notifications panel
}

const toggleUserMenu = () => {
  // Toggle user menu
}
</script>

<style scoped>
.navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-left, .nav-right {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color);
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  text-decoration: none;
  color: var(--text-color);
  font-weight: 500;
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: var(--primary-color);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.notifications {
  position: relative;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
}

.badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: var(--primary-color);
  color: white;
  font-size: 0.7rem;
  padding: 2px 5px;
  border-radius: 10px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-weight: 500;
}

.auth-buttons {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-login {
  color: var(--primary-color);
}

.btn-signup {
  background: var(--primary-color);
  color: white;
}

.btn-signup:hover {
  background: var(--primary-color);
  opacity: 0.9;
}
</style> 