<template>
  <div class="post-detail">
    <div class="post-header">
      <h1>{{ postTitle }}</h1>
      <div class="post-meta">
        <span class="date">{{ formattedDate }}</span>
        <span class="views">{{ viewsCount }} views</span>
      </div>
    </div>
    
    <div class="post-content">
      <div class="post-text">{{ postText }}</div>
      <div class="post-metrics">
        <div class="metric">
          <span class="label">Likes</span>
          <span class="value">{{ likesCount }}</span>
        </div>
        <div class="metric">
          <span class="label">Shares</span>
          <span class="value">{{ sharesCount }}</span>
        </div>
        <div class="metric">
          <span class="label">Comments</span>
          <span class="value">{{ commentsCount }}</span>
        </div>
        <div class="metric">
          <span class="label">CTR</span>
          <span class="value">{{ ctr }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const postId = route.params.id

const postTitle = ref('Post Title')
const postText = ref('Post content goes here...')
const postDate = ref(new Date())
const viewsCount = ref(0)
const likesCount = ref(0)
const sharesCount = ref(0)
const commentsCount = ref(0)
const ctr = ref(0)

const formattedDate = computed(() => {
  return postDate.value.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

// Component logic here
</script>

<style scoped>
.post-detail {
  padding: 2rem;
}

.post-header {
  margin-bottom: 2rem;
}

h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: var(--primary-color);
}

.post-meta {
  display: flex;
  gap: 1rem;
  color: var(--text-color);
  opacity: 0.8;
  font-size: 0.9rem;
}

.post-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.post-text {
  margin-bottom: 2rem;
  line-height: 1.6;
}

.post-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.metric {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.metric .label {
  font-size: 0.9rem;
  color: var(--text-color);
  opacity: 0.8;
}

.metric .value {
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--secondary-color);
}
</style> 