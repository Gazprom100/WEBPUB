import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignupView.vue')
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('../views/ForgotPasswordView.vue')
    },
    {
      path: '/channels',
      name: 'channels',
      component: () => import('../views/ChannelsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/add-channel',
      name: 'add-channel',
      component: () => import('../views/AddChannelView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/channels/:id/feed',
      name: 'channel-feed',
      component: () => import('../views/ChannelFeedView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/channels/:id/analytics',
      name: 'channel-analytics',
      component: () => import('../views/ChannelAnalyticsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/channels/:id/posts/new',
      name: 'create-channel-post',
      component: () => import('../views/PostEditorView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/channels/:id/posts/edit/:postId',
      name: 'edit-channel-post',
      component: () => import('../views/PostEditorView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/channels/:id',
      name: 'channel-detail',
      component: () => import('../views/ChannelDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/posts/:id',
      name: 'post-detail',
      component: () => import('../views/PostDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/create-post',
      name: 'create-post',
      component: () => import('../views/CreatePostView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: () => import('../views/AnalyticsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/monetization',
      name: 'monetization',
      component: () => import('../views/MonetizationView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// Защита маршрутов
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Проверяем токен при первой загрузке
  if (!authStore.isAuthenticated && localStorage.getItem('token')) {
    try {
      await authStore.checkAuth()
    } catch (error) {
      console.error('Failed to restore auth state:', error)
    }
  }

  // Если маршрут требует авторизации
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authStore.isAuthenticated) {
      // Сохраняем целевой маршрут для редиректа после входа
      next({ 
        name: 'login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    // Если пользователь авторизован и пытается зайти на страницу входа/регистрации
    if (authStore.isAuthenticated && (to.name === 'login' || to.name === 'signup')) {
      next({ name: 'channels' })
    } else {
      next()
    }
  }
})

export default router 