<template>
  <nav class="navigation">
    <div class="nav-left">
      <router-link to="/" class="logo">
        WEBPUB
      </router-link>
      <div class="nav-links">
        <router-link to="/channels">Каналы</router-link>
        <router-link to="/scheduler">Планировщик</router-link>
        <router-link to="/content-library">Библиотека</router-link>
        <router-link to="/analytics">Аналитика</router-link>
        <router-link to="/monetization">Монетизация</router-link>
      </div>
    </div>
    <div class="nav-right">
      <div class="user-menu" v-if="isAuthenticated">
        <button class="nav-icon-btn" @click="navigateTo('/settings/bot')">
          <span class="icon">🤖</span>
          <span class="tooltip">Настройки бота</span>
        </button>
        <button class="notifications" @click="toggleNotifications">
          <span class="icon">🔔</span>
          <span v-if="unreadNotifications" class="badge">{{ unreadNotifications }}</span>
          <span class="tooltip">Уведомления</span>
        </button>
        <div class="user-profile" @click="toggleUserMenu">
          <img :src="userAvatar" :alt="userName" class="avatar">
          <span class="user-name">{{ userName }}</span>
          <div v-if="showUserMenu" class="user-dropdown">
            <router-link to="/profile" class="dropdown-item">
              <span class="icon">👤</span> Профиль
            </router-link>
            <router-link to="/settings" class="dropdown-item">
              <span class="icon">⚙️</span> Настройки
            </router-link>
            <button @click="logout" class="dropdown-item logout">
              <span class="icon">🚪</span> Выйти
            </button>
          </div>
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
import { useRouter } from 'vue-router'

const router = useRouter()
const auth = useAuthStore()
const isAuthenticated = computed(() => auth.isAuthenticated)
const userName = computed(() => auth.user?.name || '')
const userAvatar = computed(() => auth.user?.avatar || '/default-avatar.png')
const unreadNotifications = ref(2)
const showUserMenu = ref(false)

const toggleNotifications = () => {
  // Toggle notifications panel
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const navigateTo = (path) => {
  router.push(path)
}

const logout = async () => {
  await auth.logout()
  router.push('/login')
}

// Close menu when clicked outside
window.addEventListener('click', (e) => {
  const userProfile = document.querySelector('.user-profile')
  if (userProfile && !userProfile.contains(e.target) && showUserMenu.value) {
    showUserMenu.value = false
  }
})
</script>

<style scoped>
.navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
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

.nav-icon-btn, .notifications {
  position: relative;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.nav-icon-btn:hover, .notifications:hover {
  background-color: #f1f5f9;
}

.tooltip {
  position: absolute;
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s;
  pointer-events: none;
}

.nav-icon-btn:hover .tooltip,
.notifications:hover .tooltip {
  opacity: 1;
  visibility: visible;
  bottom: -25px;
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
  position: relative;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.user-profile:hover {
  background-color: #f1f5f9;
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

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 180px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 0.5rem 0;
  margin-top: 0.5rem;
  z-index: 10;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  color: var(--text-color);
  text-decoration: none;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #f1f5f9;
}

.dropdown-item.logout {
  color: #e53e3e;
  border-top: 1px solid #e2e8f0;
  margin-top: 0.5rem;
  width: 100%;
  text-align: left;
  background: none;
  cursor: pointer;
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

@media (max-width: 900px) {
  .nav-links {
    display: none;
  }
}
</style> 