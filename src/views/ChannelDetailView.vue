<template>
  <div class="channel-detail">
    <div class="channel-header">
      <h1>{{ channelName }}</h1>
      <div class="channel-stats">
        <div class="stat">
          <span class="label">Subscribers</span>
          <span class="value">{{ subscribersCount }}</span>
        </div>
        <div class="stat">
          <span class="label">Posts</span>
          <span class="value">{{ postsCount }}</span>
        </div>
      </div>
    </div>
    
    <div class="posts-list">
      <!-- Posts will be listed here -->
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const channelId = route.params.id

const channelName = ref('Channel Name')
const subscribersCount = ref(0)
const postsCount = ref(0)

// Component logic here
</script>

<style scoped>
.channel-detail {
  padding: 2rem;
}

.channel-header {
  margin-bottom: 2rem;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.channel-stats {
  display: flex;
  gap: 2rem;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat .label {
  font-size: 0.9rem;
  color: var(--text-color);
  opacity: 0.8;
}

.stat .value {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--secondary-color);
}

.posts-list {
  display: grid;
  gap: 1rem;
}
</style> 