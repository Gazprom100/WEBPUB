import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/channels',
      name: 'channels',
      component: () => import('../views/ChannelsView.vue')
    },
    {
      path: '/channels/:id',
      name: 'channel-detail',
      component: () => import('../views/ChannelDetailView.vue')
    },
    {
      path: '/posts/:id',
      name: 'post-detail',
      component: () => import('../views/PostDetailView.vue')
    }
  ]
})

export default router 